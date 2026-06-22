"""
OPES Health Systems — Phase 3: Self-Improvement Engine (Darwin Gödel Machine)

Every run, each AI employee's system prompt is:
  1. Tested against a standard benchmark task
  2. Scored on 5 dimensions (0–100 total)
  3. Mutated to fix the weakest dimension
  4. Re-tested with the mutant prompt
  5. Winner (original vs mutant) is kept — loser is discarded

Over time, prompts evolve to produce better and better output.
The evolutionary history is stored in evolution_log.json.

Usage:
    python self_improve.py                          # evolve all 8 agents
    python self_improve.py amara                    # evolve one agent
    python self_improve.py amara kofi emeka         # evolve specific agents
    python self_improve.py --status                 # show evolution history
    python self_improve.py --rollback amara 3       # restore agent to generation 3
"""

from __future__ import annotations

import sys
from pathlib import Path

from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

load_dotenv()

console = Console()

ROOT = Path(__file__).parent
PROMPTS_DIR = ROOT / "config" / "prompts"
BACKUP_DIR = ROOT / "improver" / "prompt_history"


def _status():
    from improver.evolution_store import EvolutionStore
    store = EvolutionStore()
    summary = store.summary()

    console.print(Panel(
        f"Total generations run: [bold]{summary['total_generations']}[/bold]\n"
        f"Mutation adoption rate: [bold]{summary['adoption_rate']*100:.1f}%[/bold]",
        title="OPES Evolution Summary",
        border_style="green",
    ))

    if not summary["by_agent"]:
        console.print("[dim]No evolution history yet. Run self_improve.py to start.[/dim]")
        return

    table = Table(border_style="cyan")
    table.add_column("Agent", style="bold white")
    table.add_column("Generations", justify="right")
    table.add_column("Adopted", justify="right", style="green")
    table.add_column("Avg Δ Score", justify="right")
    table.add_column("Champion Gen", justify="right")

    emojis = {
        "amara": "📱", "chisom": "💬", "kofi": "🎯", "zara": "✍️",
        "emeka": "🔍", "fatima": "💛", "atlas": "🌍", "nova": "📊",
    }
    champions = summary.get("champions", {})

    for agent, stats in summary["by_agent"].items():
        champ = champions.get(agent, {})
        champ_gen = str(champ.get("generation", "—"))
        delta_str = f"+{stats['avg_improvement']}" if stats['avg_improvement'] >= 0 else str(stats['avg_improvement'])
        emoji = emojis.get(agent, "🤖")
        table.add_row(
            f"{emoji} {agent.upper()}",
            str(stats["generations"]),
            str(stats["adopted"]),
            delta_str,
            champ_gen,
        )
    console.print(table)

    # Per-agent generation history
    store2 = EvolutionStore()
    for agent in summary["by_agent"]:
        history = store2.agent_history(agent)
        if not history:
            continue
        console.print(f"\n[bold]{agent.upper()}[/bold] evolution log:")
        for g in history[-5:]:  # show last 5
            icon = "✓" if g["adopted"] else "✗"
            console.print(
                f"  Gen {g['generation']:02d} [{icon}] "
                f"original={g['original_score']} → mutant={g['mutant_score']} "
                f"({g['mutation_summary']})"
            )


def _rollback(agent: str, generation: int):
    backup = BACKUP_DIR / f"{agent}_gen{generation:03d}_original.md"
    if not backup.exists():
        console.print(f"[red]No backup found: {backup}[/red]")
        sys.exit(1)

    from improver.ab_tester import AGENT_PROMPT_FILES
    prompt_path = PROMPTS_DIR / AGENT_PROMPT_FILES[agent]
    prompt_path.write_text(backup.read_text(encoding="utf-8"), encoding="utf-8")
    console.print(f"[green]✓ {agent.upper()} rolled back to generation {generation}[/green]")


def _evolve(agents: list[str]):
    from improver.ab_tester import ABTester, AGENT_PROMPT_FILES
    from improver.benchmarks import BENCHMARK_TASKS

    tester = ABTester()

    console.print(Panel(
        "[bold green]OPES Phase 3 — Darwin Gödel Machine[/bold green]\n"
        "Each agent's prompt will be evaluated, mutated, and improved.\n"
        "The fittest prompt survives.",
        border_style="green",
    ))

    for agent in agents:
        if agent not in AGENT_PROMPT_FILES:
            console.print(f"[red]Unknown agent: {agent}[/red]")
            continue

        task = BENCHMARK_TASKS.get(agent, "Demonstrate your core capability for Opes Health Systems.")

        console.rule(f"[bold cyan]{agent.upper()}[/bold cyan]")
        try:
            result = tester.run(agent, task, verbose=True)
            icon = "✓ IMPROVED" if result["winner"] == "mutant" else "— No change"
            color = "green" if result["winner"] == "mutant" else "dim"
            console.print(
                f"[{color}]{icon}[/{color}] "
                f"{result['original_score']} → {result['mutant_score']} "
                f"({result['delta']:+.1f}) | {result['mutation_summary']}"
            )
        except Exception as e:
            console.print(f"[red]Error evolving {agent}: {e}[/red]")

    console.print("\n[green]Evolution complete. Run 'python self_improve.py --status' to see history.[/green]")


def main():
    args = sys.argv[1:]

    if not args or args == ["--all"]:
        from improver.ab_tester import AGENT_PROMPT_FILES
        _evolve(list(AGENT_PROMPT_FILES.keys()))
        return

    if args[0] == "--status":
        _status()
        return

    if args[0] == "--rollback":
        if len(args) < 3:
            console.print("[red]Usage: python self_improve.py --rollback <agent> <generation>[/red]")
            sys.exit(1)
        _rollback(args[1].lower(), int(args[2]))
        return

    # Otherwise treat arguments as agent names
    agents = [a.lower() for a in args]
    _evolve(agents)


if __name__ == "__main__":
    main()
