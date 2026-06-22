"""
ABTester — runs the same task with original and mutant prompt, scores both,
declares a winner, and saves the winning prompt to disk.

The evolutionary loop:
  original prompt → score → mutate → score mutant → compare → save winner
"""

from __future__ import annotations

import hashlib
import os
from pathlib import Path

import anthropic
import yaml

from .evaluator import PromptEvaluator
from .evolver import PromptEvolver
from .evolution_store import EvolutionStore

ROOT = Path(__file__).parent.parent
CONFIG_DIR = ROOT / "config"
PROMPTS_DIR = CONFIG_DIR / "prompts"
PROMPT_BACKUP_DIR = ROOT / "improver" / "prompt_history"
PROMPT_BACKUP_DIR.mkdir(exist_ok=True)

AGENT_PROMPT_FILES = {
    "amara":  "amara_social.md",
    "chisom": "chisom_service.md",
    "kofi":   "kofi_marketing.md",
    "zara":   "zara_content.md",
    "emeka":  "emeka_leads.md",
    "fatima": "fatima_outreach.md",
    "atlas":  "atlas_research.md",
    "nova":   "nova_analytics.md",
}

IMPROVEMENT_THRESHOLD = 3.0  # mutant must beat original by this many points to be adopted


def _load_company_context() -> str:
    with open(CONFIG_DIR / "company.yaml") as f:
        data = yaml.safe_load(f)
    return yaml.dump(data, allow_unicode=True, sort_keys=False)


def _build_full_prompt(agent_prompt: str) -> str:
    company_yaml = _load_company_context()
    return (
        agent_prompt
        + "\n\n---\n## COMPANY KNOWLEDGE BASE\n\n"
        + f"```yaml\n{company_yaml}\n```\n---\n"
    )


def _run_task_with_prompt(system_prompt: str, task: str) -> str:
    """Run a single task against a given system prompt and return the output."""
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4096,
        system=system_prompt,
        messages=[{"role": "user", "content": task}],
    )
    return "\n".join(b.text for b in response.content if b.type == "text").strip()


def _sha8(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:8]


def _backup_prompt(agent: str, generation: int, prompt: str, label: str) -> None:
    filename = PROMPT_BACKUP_DIR / f"{agent}_gen{generation:03d}_{label}.md"
    filename.write_text(prompt, encoding="utf-8")


class ABTester:
    def __init__(self) -> None:
        self.evaluator = PromptEvaluator()
        self.evolver = PromptEvolver()
        self.store = EvolutionStore()

    def run(self, agent: str, task: str, verbose: bool = True) -> dict:
        """
        Run one full generation of the evolutionary loop for an agent.

        Steps:
          1. Load current prompt from disk
          2. Run task → score output
          3. Generate mutant prompt targeting weakest dimension
          4. Run same task with mutant → score output
          5. Compare — adopt mutant if it beats original by threshold
          6. Save winner prompt to disk, log to evolution store

        Returns a result dict with all scores and winner info.
        """
        prompt_file = AGENT_PROMPT_FILES.get(agent)
        if not prompt_file:
            raise ValueError(f"Unknown agent: {agent}. Must be one of {list(AGENT_PROMPT_FILES)}")

        prompt_path = PROMPTS_DIR / prompt_file

        # 1. Load current prompt
        original_agent_prompt = prompt_path.read_text(encoding="utf-8")
        original_full_prompt = _build_full_prompt(original_agent_prompt)

        generation = len(self.store.agent_history(agent)) + 1

        if verbose:
            print(f"\n[Gen {generation}] Running original {agent.upper()} on task...")

        # 2. Run task with original prompt
        original_output = _run_task_with_prompt(original_full_prompt, task)
        original_scores = self.evaluator.score(task, original_output)

        if verbose:
            print(f"  Original score: {original_scores['total']}/100 — {original_scores['reasoning']}")

        # 3. Generate mutant prompt
        if verbose:
            print(f"  Generating mutation targeting weak dimension...")

        mutant_agent_prompt, weakest_dim, mutation_summary = self.evolver.mutate(
            current_prompt=original_agent_prompt,
            scores=original_scores,
            task=task,
            output=original_output,
        )
        mutant_full_prompt = _build_full_prompt(mutant_agent_prompt)

        # 4. Run task with mutant
        if verbose:
            print(f"  Running mutant {agent.upper()} ({mutation_summary})...")

        mutant_output = _run_task_with_prompt(mutant_full_prompt, task)
        mutant_scores = self.evaluator.score(task, mutant_output)

        if verbose:
            print(f"  Mutant score:   {mutant_scores['total']}/100 — {mutant_scores['reasoning']}")

        # 5. Compare and decide winner
        delta = mutant_scores["total"] - original_scores["total"]
        if delta >= IMPROVEMENT_THRESHOLD:
            winner = "mutant"
            winning_agent_prompt = mutant_agent_prompt
            if verbose:
                print(f"  ✓ MUTANT WINS (+{delta:.1f} pts). Adopting new prompt.")
        else:
            winner = "original"
            winning_agent_prompt = original_agent_prompt
            if verbose:
                print(f"  ✗ Original holds ({delta:+.1f} pts below threshold of {IMPROVEMENT_THRESHOLD}).")

        # 6. Backup both versions
        _backup_prompt(agent, generation, original_agent_prompt, "original")
        _backup_prompt(agent, generation, mutant_agent_prompt, "mutant")

        # 7. Save winning prompt to disk (only overwrites if mutant won)
        if winner == "mutant":
            prompt_path.write_text(mutant_agent_prompt, encoding="utf-8")

        # 8. Log to evolution store
        self.store.record_generation(
            agent=agent,
            generation=generation,
            task=task,
            original_score=original_scores["total"],
            mutant_score=mutant_scores["total"],
            winner=winner,
            mutation_summary=mutation_summary,
            original_prompt_hash=_sha8(original_agent_prompt),
            mutant_prompt_hash=_sha8(mutant_agent_prompt),
        )

        return {
            "agent": agent,
            "generation": generation,
            "task": task,
            "original_score": original_scores["total"],
            "mutant_score": mutant_scores["total"],
            "winner": winner,
            "delta": delta,
            "weakest_dimension": weakest_dim,
            "mutation_summary": mutation_summary,
            "original_output": original_output,
            "mutant_output": mutant_output,
            "original_scores": original_scores,
            "mutant_scores": mutant_scores,
        }

    def run_full_team(self, tasks: dict[str, str], verbose: bool = True) -> list[dict]:
        """
        Run one generation for all agents simultaneously.
        tasks: {agent_name: benchmark_task_string}
        """
        results = []
        for agent, task in tasks.items():
            try:
                result = self.run(agent, task, verbose=verbose)
                results.append(result)
            except Exception as e:
                if verbose:
                    print(f"  [ERROR] {agent.upper()} evolution failed: {e}")
        return results
