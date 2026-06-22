"""
AgentPipeline — chains agents so the output of one feeds the next.

Each step in a pipeline is:
  {
    "agent":   agent_name,          # "amara", "kofi", etc.
    "task_fn": callable | str,      # callable(context) -> str task, or literal str
    "label":   str,                 # human-readable name for this step
    "store_as": str | None,         # key to store output in shared context
  }

The shared context dict accumulates all outputs and is available to every
downstream step, enabling true agent-to-agent communication.
"""

from __future__ import annotations

import time
from datetime import datetime
from pathlib import Path
from typing import Any, Callable

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

OUTPUT_DIR = Path(__file__).parent.parent / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

AGENT_EMOJIS = {
    "amara": "📱", "chisom": "💬", "kofi": "🎯", "zara": "✍️",
    "emeka": "🔍", "fatima": "💛", "atlas": "🌍", "nova": "📊",
}


def _load_agent(name: str):
    from agents import (
        AmaraSocialAgent, ChisomServiceAgent, KofiMarketingAgent,
        ZaraContentAgent, EmekaLeadsAgent, FatimaOutreachAgent,
        AtlasResearchAgent, NovaAnalyticsAgent,
    )
    registry = {
        "amara": AmaraSocialAgent,
        "chisom": ChisomServiceAgent,
        "kofi": KofiMarketingAgent,
        "zara": ZaraContentAgent,
        "emeka": EmekaLeadsAgent,
        "fatima": FatimaOutreachAgent,
        "atlas": AtlasResearchAgent,
        "nova": NovaAnalyticsAgent,
    }
    cls = registry.get(name.lower())
    if not cls:
        raise ValueError(f"Unknown agent: {name}")
    return cls()


class AgentPipeline:
    """
    Runs a sequence of agents, passing context between them.

    Usage:
        pipeline = AgentPipeline("new_lead_workflow")
        pipeline.add_step("emeka",  task_fn=lambda ctx: f"Research {ctx['company']}...", store_as="lead_research")
        pipeline.add_step("fatima", task_fn=lambda ctx: f"Using this research:\n{ctx['lead_research']}\nCreate onboarding...", store_as="onboarding")
        result = pipeline.run({"company": "Clinique Sainte-Marie"})
    """

    def __init__(self, name: str) -> None:
        self.name = name
        self.steps: list[dict[str, Any]] = []
        self._log: list[dict] = []

    def add_step(
        self,
        agent: str,
        task_fn: Callable[[dict], str] | str,
        label: str = "",
        store_as: str | None = None,
    ) -> "AgentPipeline":
        self.steps.append({
            "agent": agent.lower(),
            "task_fn": task_fn,
            "label": label or f"{agent.upper()} step",
            "store_as": store_as or f"{agent}_output_{len(self.steps)}",
        })
        return self

    def run(self, initial_context: dict | None = None, verbose: bool = True) -> dict:
        """
        Execute the pipeline. Returns the final shared context dict.
        All agent outputs are stored in context[step['store_as']].
        """
        context: dict[str, Any] = initial_context or {}
        context["_pipeline"] = self.name
        context["_started_at"] = datetime.utcnow().isoformat()
        context["_step_results"] = []

        if verbose:
            console.print(Panel(
                f"[bold green]Pipeline: {self.name}[/bold green]\n"
                f"{len(self.steps)} agents · starting now",
                border_style="green",
            ))

        for i, step in enumerate(self.steps, 1):
            agent_name = step["agent"]
            emoji = AGENT_EMOJIS.get(agent_name, "🤖")
            label = step["label"]

            if verbose:
                console.rule(f"[cyan]Step {i}/{len(self.steps)} — {emoji} {agent_name.upper()} — {label}[/cyan]")

            # Build the task string
            if callable(step["task_fn"]):
                task = step["task_fn"](context)
            else:
                task = step["task_fn"]

            # Run the agent
            t0 = time.time()
            agent = _load_agent(agent_name)

            with Progress(
                SpinnerColumn(),
                TextColumn(f"[green]{agent_name.upper()} working...[/green]"),
                transient=True,
                console=console,
            ) as progress:
                progress.add_task("", total=None)
                output = agent.run_task(task, store_memory=True)

            elapsed = round(time.time() - t0, 1)

            # Store output in context
            key = step["store_as"]
            context[key] = output

            step_record = {
                "step": i,
                "agent": agent_name,
                "label": label,
                "task_preview": task[:200],
                "output_preview": output[:300],
                "elapsed_s": elapsed,
                "store_as": key,
            }
            context["_step_results"].append(step_record)
            self._log.append(step_record)

            if verbose:
                console.print(f"[dim]✓ {elapsed}s — output stored as '{key}'[/dim]")

        context["_completed_at"] = datetime.utcnow().isoformat()

        # Save combined pipeline output
        self._save_pipeline_output(context)

        if verbose:
            console.print(Panel(
                f"[bold green]Pipeline complete: {self.name}[/bold green]\n"
                f"All outputs saved to outputs/",
                border_style="green",
            ))

        return context

    def _save_pipeline_output(self, context: dict) -> None:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = OUTPUT_DIR / f"pipeline_{self.name}_{ts}.md"
        lines = [
            f"# Pipeline: {self.name}",
            f"**Started:** {context.get('_started_at', '')}",
            f"**Completed:** {context.get('_completed_at', '')}",
            "",
        ]
        for record in context.get("_step_results", []):
            lines += [
                f"---",
                f"## Step {record['step']}: {record['agent'].upper()} — {record['label']}",
                f"**Task:** {record['task_preview']}{'...' if len(record['task_preview']) == 200 else ''}",
                "",
                context.get(record["store_as"], ""),
                "",
            ]
        filename.write_text("\n".join(lines), encoding="utf-8")
