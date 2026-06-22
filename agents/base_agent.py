"""
Base agent class — all 8 Opes AI employees inherit from this.
Phase 2: memory-aware. Every agent remembers past interactions,
learns from outcomes, and recalls relevant context before responding.
"""

from __future__ import annotations

import os
import yaml
from pathlib import Path
from typing import Any

import anthropic
from rich.console import Console
from rich.panel import Panel

from memory import AgentMemory

console = Console()

ROOT = Path(__file__).parent.parent
CONFIG_DIR = ROOT / "config"
PROMPTS_DIR = CONFIG_DIR / "prompts"


def _load_company_context() -> dict:
    with open(CONFIG_DIR / "company.yaml") as f:
        return yaml.safe_load(f)


class BaseAgent:
    """
    Foundation for all Opes Health Systems AI employees.

    Phase 2 additions:
    - Persistent memory (ChromaDB vector store, local/offline)
    - Automatic recall of relevant past context before each task
    - Automatic storage of interactions after each task
    - learn(), remember_success(), remember_entity() helpers
    """

    name: str = "Base"
    role: str = "AI Employee"
    emoji: str = "🤖"
    prompt_file: str = ""
    model: str = "claude-sonnet-4-6"

    def __init__(self) -> None:
        self.client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
        self.company = _load_company_context()
        self.system_prompt = self._build_system_prompt()
        self.history: list[dict[str, Any]] = []
        self.memory = AgentMemory(self.name)

    # ── System prompt ────────────────────────────────────────────────────────

    def _build_system_prompt(self) -> str:
        prompt_path = PROMPTS_DIR / self.prompt_file
        agent_prompt = prompt_path.read_text()
        company_yaml = yaml.dump(self.company, allow_unicode=True, sort_keys=False)
        company_context = (
            "\n---\n"
            "## COMPANY KNOWLEDGE BASE\n\n"
            f"```yaml\n{company_yaml}\n```\n"
            "---\n"
        )
        return agent_prompt + company_context

    # ── Core think ───────────────────────────────────────────────────────────

    def think(self, message: str, tools: list[dict] | None = None) -> str:
        self.history.append({"role": "user", "content": message})
        kwargs: dict[str, Any] = {
            "model": self.model,
            "max_tokens": 8096,
            "system": self.system_prompt,
            "messages": self.history,
        }
        if tools:
            kwargs["tools"] = tools
        response = self.client.messages.create(**kwargs)
        parts = [b.text for b in response.content if b.type == "text"]
        reply = "\n".join(parts).strip()
        self.history.append({"role": "assistant", "content": response.content})
        return reply

    # ── Memory-aware task runner ─────────────────────────────────────────────

    def run_task(self, task: str, store_memory: bool = True) -> str:
        """
        Run a task with automatic memory injection and storage.

        Before thinking: retrieves relevant past memories and injects them.
        After thinking:  stores the interaction so future sessions remember it.
        """
        self.reset()

        # 1. Retrieve relevant memories
        recalled = self.memory.recall(task, n=4)
        what_worked = self.memory.recall_what_worked(task, n=2)
        recent = self.memory.recent_history(n=3)

        # 2. Build memory-enriched message
        memory_block = ""
        if recalled or what_worked or recent:
            memory_block = (
                "\n\n---\n"
                "## YOUR MEMORY (from past sessions)\n"
                "Use this context to give better, more specific answers.\n\n"
            )
            if recent:
                memory_block += recent + "\n\n"
            if recalled:
                memory_block += recalled + "\n\n"
            if what_worked:
                memory_block += what_worked + "\n\n"
            memory_block += "---\n\n"

        enriched_task = memory_block + task if memory_block else task

        # 3. Think
        result = self.think(enriched_task)

        # 4. Store this interaction in memory
        if store_memory:
            summary = result[:500] + "..." if len(result) > 500 else result
            self.memory.remember_interaction(
                task=task,
                result_summary=summary,
                outcome="completed",
            )

        self.display(result)
        return result

    # ── Memory shortcuts for subclasses ──────────────────────────────────────

    def learn(self, insight: str, source: str = "") -> None:
        """Store a learned insight for future sessions."""
        self.memory.learn(insight, source=source)

    def remember_success(self, approach: str, result: str, context: str = "") -> None:
        """Store a winning approach for future reference."""
        self.memory.remember_success(approach, result, context)

    def remember_entity(self, entity_type: str, name: str, details: str) -> None:
        """Store a customer, lead, or competitor."""
        self.memory.remember_entity(entity_type, name, details)

    def recall(self, query: str, n: int = 5) -> str:
        """Manually retrieve memories relevant to a query."""
        return self.memory.recall(query, n=n)

    # ── Utilities ────────────────────────────────────────────────────────────

    def reset(self) -> None:
        """Clear conversation history (not memory — memory persists)."""
        self.history = []

    def memory_stats(self) -> dict:
        return self.memory.stats()

    def display(self, message: str) -> None:
        mem_count = self.memory.store.count()
        title = f"{self.emoji} {self.name} | {self.role} | 🧠 {mem_count} memories"
        console.print(Panel(message, title=title, border_style="green"))
