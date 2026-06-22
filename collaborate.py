"""
OPES Health Systems — Phase 4: Multi-Agent Collaboration

The AI employees now work TOGETHER, passing intelligence between each other
to complete complex tasks no single agent could handle alone.

Usage:
    # Natural language — router picks the right workflow automatically:
    python collaborate.py "We found a tender from the Gabon Ministry of Health for hospital software"
    python collaborate.py "New lead: Dr. Bello at Lagos General Hospital, interested in OPES EMR"
    python collaborate.py "OpenMRS just launched a free tier targeting African hospitals"

    # Direct workflow with parameters:
    python collaborate.py --workflow new_lead --lead-name "Dr. Bello" --company "Lagos General" --country "Nigeria" --product "OPES EMR"
    python collaborate.py --workflow tender_found --tender-title "HIS for 5 regional hospitals" --issuer "Ministry of Health Gabon" --country "Gabon" --deadline "2026-08-15"
    python collaborate.py --workflow content_campaign --product "OPES PHARMIS" --goal "20 demo bookings" --audience "pharmacy directors in Cameroon" --duration "30 days"
    python collaborate.py --workflow competitor_alert --competitor "OpenMRS" --threat "launched free tier" --affected-products "OPES EMR, OPES HIS"
    python collaborate.py --workflow market_expansion --country "Gabon" --product-focus "OPES EMR"
    python collaborate.py --workflow weekly_review --week "Week 26, June 2026"

    # List available workflows:
    python collaborate.py --list
"""

from __future__ import annotations

import sys

from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

load_dotenv()

console = Console()


def show_list():
    from orchestrator.workflows import WORKFLOWS

    table = Table(title="Available Multi-Agent Workflows", border_style="green")
    table.add_column("ID", style="bold cyan", width=20)
    table.add_column("Description", style="white")
    table.add_column("Agents", style="dim")

    agent_map = {
        "new_lead": "EMEKA → FATIMA → KOFI → NOVA",
        "tender_found": "ATLAS → NOVA → ZARA → KOFI",
        "content_campaign": "KOFI → ZARA → AMARA",
        "competitor_alert": "ATLAS → NOVA → KOFI → CHISOM",
        "customer_crisis": "CHISOM → FATIMA → NOVA",
        "market_expansion": "ATLAS → EMEKA → KOFI → NOVA",
        "weekly_review": "ATLAS → EMEKA → AMARA → NOVA",
        "custom": "NOVA (auto-routes)",
    }

    for wid, meta in WORKFLOWS.items():
        table.add_row(wid, meta["description"], agent_map.get(wid, ""))
    console.print(table)
    console.print("\n[dim]Run any workflow with: python collaborate.py \"<natural language goal>\"[/dim]")
    console.print("[dim]Or directly: python collaborate.py --workflow <id> [--param value ...][/dim]")


def _parse_kwargs(args: list[str]) -> dict:
    """Parse --key value pairs from CLI args into a dict."""
    params = {}
    i = 0
    while i < len(args):
        if args[i].startswith("--"):
            key = args[i][2:].replace("-", "_")
            if i + 1 < len(args) and not args[i + 1].startswith("--"):
                params[key] = args[i + 1]
                i += 2
            else:
                params[key] = True
                i += 1
        else:
            i += 1
    return params


def main():
    args = sys.argv[1:]

    if not args or args[0] in ("-h", "--help"):
        console.print(Panel(__doc__.strip(), border_style="green"))
        return

    if args[0] == "--list":
        show_list()
        return

    # Direct workflow mode
    if args[0] == "--workflow":
        if len(args) < 2:
            console.print("[red]Specify a workflow ID after --workflow[/red]")
            sys.exit(1)
        workflow_id = args[1]
        params = _parse_kwargs(args[2:])

        from orchestrator.workflows import WORKFLOWS, build_workflow
        if workflow_id not in WORKFLOWS:
            console.print(f"[red]Unknown workflow: {workflow_id}[/red]")
            show_list()
            sys.exit(1)

        pipeline = build_workflow(workflow_id, params)
        pipeline.run(params)
        return

    # Natural language mode — join all non-flag args as the goal
    goal = " ".join(a for a in args if not a.startswith("--"))
    if not goal:
        console.print(Panel(__doc__.strip(), border_style="green"))
        return

    console.print(Panel(
        f"[bold green]Goal:[/bold green] {goal}\n\n"
        f"[dim]Routing to best workflow...[/dim]",
        border_style="green",
    ))

    from orchestrator.router import WorkflowRouter
    router = WorkflowRouter()
    router.route(goal)


if __name__ == "__main__":
    main()
