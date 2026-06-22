"""
Memory CLI — inspect, search, and manage agent memories.

Usage:
    python memory_cli.py stats
    python memory_cli.py recall <agent> "<query>"
    python memory_cli.py recent <agent> [n]
    python memory_cli.py learn <agent> "<insight>"
    python memory_cli.py seed <agent> <file.txt>
    python memory_cli.py clear <agent>

Agents: amara, chisom, kofi, zara, emeka, fatima, atlas, nova
"""

from __future__ import annotations

import sys
from pathlib import Path

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from memory import AgentMemory

console = Console()

ALL_AGENTS = ["amara", "chisom", "kofi", "zara", "emeka", "fatima", "atlas", "nova"]

AGENT_EMOJIS = {
    "amara": "📱", "chisom": "💬", "kofi": "🎯",
    "zara": "✍️",  "emeka": "🔍", "fatima": "💛",
    "atlas": "🌍", "nova": "📊",
}


def cmd_stats():
    """Show memory counts for all 8 agents."""
    table = Table(title="OPES Agent Memory Summary", border_style="green")
    table.add_column("Agent", style="bold cyan")
    table.add_column("Role", style="dim")
    table.add_column("Memories", justify="right", style="bold white")

    roles = {
        "amara": "Social Media Manager",
        "chisom": "Customer Service Rep",
        "kofi": "Marketing Strategist",
        "zara": "Content Creator",
        "emeka": "Lead Generation",
        "fatima": "Customer Outreach",
        "atlas": "Research & Intel",
        "nova": "Business Intelligence",
    }

    total = 0
    for name in ALL_AGENTS:
        mem = AgentMemory(name)
        count = mem.store.count()
        total += count
        emoji = AGENT_EMOJIS[name]
        table.add_row(f"{emoji} {name.upper()}", roles[name], str(count))

    table.add_section()
    table.add_row("[bold]TOTAL[/bold]", "", f"[bold green]{total}[/bold green]")
    console.print(table)


def cmd_recall(agent: str, query: str, n: int = 5):
    """Retrieve memories relevant to a query."""
    mem = AgentMemory(agent)
    result = mem.recall(query, n=n)
    if result:
        console.print(Panel(result, title=f"🧠 {agent.upper()} memories for: '{query}'", border_style="cyan"))
    else:
        console.print(f"[dim]No memories found for '{query}'[/dim]")


def cmd_recent(agent: str, n: int = 5):
    """Show most recent episodic memories."""
    mem = AgentMemory(agent)
    result = mem.recent_history(n=n)
    if result:
        console.print(Panel(result, title=f"📅 {agent.upper()} recent activity", border_style="cyan"))
    else:
        console.print(f"[dim]No recent activity for {agent.upper()}[/dim]")


def cmd_learn(agent: str, insight: str):
    """Manually seed a semantic insight into an agent's memory."""
    mem = AgentMemory(agent)
    mid = mem.learn(insight, source="manual seed")
    console.print(f"[green]✓ Insight stored for {agent.upper()} (id: {mid[:8]}...)[/green]")
    console.print(f"[dim]{insight}[/dim]")


def cmd_seed(agent: str, filepath: str):
    """
    Seed an agent from a text file.
    File format: one insight per line. Blank lines ignored. Lines starting with # ignored.
    """
    path = Path(filepath)
    if not path.exists():
        console.print(f"[red]File not found: {filepath}[/red]")
        sys.exit(1)

    lines = [l.strip() for l in path.read_text().splitlines()]
    lines = [l for l in lines if l and not l.startswith("#")]

    mem = AgentMemory(agent)
    count = 0
    for line in lines:
        mem.learn(line, source=f"seed:{path.name}")
        count += 1

    console.print(f"[green]✓ Seeded {count} insights into {agent.upper()} memory[/green]")


def cmd_clear(agent: str):
    """Delete all memories for one agent (irreversible)."""
    mem = AgentMemory(agent)
    current = mem.store.count()
    if current == 0:
        console.print(f"[dim]{agent.upper()} has no memories to clear.[/dim]")
        return

    confirm = input(f"Delete ALL {current} memories for {agent.upper()}? Type 'yes' to confirm: ")
    if confirm.strip().lower() != "yes":
        console.print("[dim]Aborted.[/dim]")
        return

    client = mem.store.collection
    ids = mem.store.collection.get(include=[])["ids"]
    if ids:
        mem.store.collection.delete(ids=ids)
    console.print(f"[green]✓ Cleared {current} memories for {agent.upper()}[/green]")


def usage():
    console.print(Panel(
        __doc__.strip(),
        title="Memory CLI — OPES Health Systems",
        border_style="green"
    ))


def main():
    args = sys.argv[1:]
    if not args:
        usage()
        return

    cmd = args[0].lower()

    if cmd == "stats":
        cmd_stats()

    elif cmd == "recall":
        if len(args) < 3:
            console.print("[red]Usage: python memory_cli.py recall <agent> \"<query>\"[/red]")
            sys.exit(1)
        agent = args[1].lower()
        query = args[2]
        n = int(args[3]) if len(args) > 3 else 5
        cmd_recall(agent, query, n)

    elif cmd == "recent":
        if len(args) < 2:
            console.print("[red]Usage: python memory_cli.py recent <agent> [n][/red]")
            sys.exit(1)
        agent = args[1].lower()
        n = int(args[2]) if len(args) > 2 else 5
        cmd_recent(agent, n)

    elif cmd == "learn":
        if len(args) < 3:
            console.print("[red]Usage: python memory_cli.py learn <agent> \"<insight>\"[/red]")
            sys.exit(1)
        cmd_learn(args[1].lower(), args[2])

    elif cmd == "seed":
        if len(args) < 3:
            console.print("[red]Usage: python memory_cli.py seed <agent> <file.txt>[/red]")
            sys.exit(1)
        cmd_seed(args[1].lower(), args[2])

    elif cmd == "clear":
        if len(args) < 2:
            console.print("[red]Usage: python memory_cli.py clear <agent>[/red]")
            sys.exit(1)
        cmd_clear(args[1].lower())

    else:
        console.print(f"[red]Unknown command: {cmd}[/red]")
        usage()
        sys.exit(1)


if __name__ == "__main__":
    main()
