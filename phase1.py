"""
OPES Health Systems — Phase 1 Launcher
Run any of the 8 AI employees interactively.

Usage:
    python phase1.py

You will be shown a menu. Pick an agent and a task.
All output is saved to outputs/ with a timestamp.
"""

import os
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

load_dotenv()
console = Console()

OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)


def check_api_key():
    key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not key or key == "your_anthropic_api_key_here":
        console.print(Panel(
            "[red]ANTHROPIC_API_KEY not set.[/red]\n\n"
            "1. Open the file: [bold].env[/bold]\n"
            "2. Replace [bold]your_anthropic_api_key_here[/bold] with your real key\n"
            "3. Get a key at: [bold]https://console.anthropic.com[/bold]\n"
            "4. Run this script again.",
            title="⚠️  Setup Required",
            border_style="red"
        ))
        sys.exit(1)


def save_output(agent_name: str, task: str, result: str) -> str:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = OUTPUT_DIR / f"{agent_name.lower()}_{ts}.md"
    filename.write_text(
        f"# {agent_name} — Output\n"
        f"**Task:** {task}\n"
        f"**Date:** {datetime.now().strftime('%d %B %Y %H:%M')}\n\n"
        f"---\n\n{result}"
    )
    return str(filename)


AGENTS = {
    "1": {
        "name": "AMARA",
        "role": "Social Media Manager",
        "emoji": "📱",
        "class": "AmaraSocialAgent",
        "quick_tasks": [
            "Create a full week LinkedIn content calendar for OPES Health Systems",
            "Write a Facebook post about OPESCare Universal Health ID in English and French",
            "Create a LinkedIn post about why African hospitals are still on paper and how OPES solves this",
            "Write a TikTok/Reels script about OPES Triage (60 seconds)",
            "Write a WhatsApp broadcast message announcing OPES PHARMIS",
        ]
    },
    "2": {
        "name": "CHISOM",
        "role": "Customer Service Rep",
        "emoji": "💬",
        "class": "ChisomServiceAgent",
        "quick_tasks": [
            "A hospital director in Yaoundé asks: what is the difference between OPES EMR and OPES Hospital HIS?",
            "A clinic owner asks: does your software work without internet?",
            "A Ministry of Health official asks: how does OPES support Cameroon's Digital Health Strategy 2026-2030?",
            "Write the top 10 FAQs for OPES Health Systems with answers",
            "A client complains that their OPES EMR is running slowly after installation",
        ]
    },
    "3": {
        "name": "KOFI",
        "role": "Marketing Strategist",
        "emoji": "🎯",
        "class": "KofiMarketingAgent",
        "quick_tasks": [
            "Build a complete campaign to get 20 demo bookings from private hospitals in Douala this month",
            "Write a 7-email welcome sequence for hospital directors who downloaded our brochure",
            "Create Facebook ad copy targeting hospital administrators in Cameroon and CEMAC",
            "Design a lead magnet: Hospital Digital Readiness Assessment for African Hospitals",
            "Write a LinkedIn ad campaign targeting Ministry of Health officials in CEMAC countries",
        ]
    },
    "4": {
        "name": "ZARA",
        "role": "Content Creator",
        "emoji": "✍️",
        "class": "ZaraContentAgent",
        "quick_tasks": [
            "Write a 1500-word SEO blog: How to choose a Hospital Information System in Cameroon",
            "Write product descriptions for all 5 Core Platform products (OPESCare, EMR, HIS, UHC IS, Triage)",
            "Write a case study: a private clinic in Douala goes from paper to OPES EMR in 90 days",
            "Write this week's email newsletter: topic — why offline-first software is critical for African hospitals",
            "Ghostwrite a LinkedIn article from the OPES founder: why we built Africa's healthcare OS in Cameroon",
        ]
    },
    "5": {
        "name": "EMEKA",
        "role": "Lead Generation",
        "emoji": "🔍",
        "class": "EmekaLeadsAgent",
        "quick_tasks": [
            "Research 20 qualified hospital leads in Cameroon (Yaoundé + Douala) with contact details",
            "Write a complete cold outreach sequence for private hospital directors in Cameroon",
            "Write a LinkedIn outreach campaign targeting hospital IT directors in CEMAC",
            "Find tender and procurement opportunities for health information systems in CEMAC region",
            "Research 15 NGO leads in Cameroon that could need GYNOBSIS, PAEDIS, or NDIS",
        ]
    },
    "6": {
        "name": "FATIMA",
        "role": "Customer Outreach & CRM",
        "emoji": "💛",
        "class": "FatimaOutreachAgent",
        "quick_tasks": [
            "Create a 30-day onboarding sequence for a new client: Clinique La Référence, Douala, bought OPES EMR",
            "Write re-engagement messages for hospitals that requested a demo but went quiet for 60 days",
            "Write a WhatsApp sequence to follow up after an OPES demo (3 messages over 2 weeks)",
            "Write a referral request to a happy PHARMIS client",
            "Create a special message for Cameroonian hospitals on Cameroon Health Day",
        ]
    },
    "7": {
        "name": "ATLAS",
        "role": "Research & Competitor Intel",
        "emoji": "🌍",
        "class": "AtlasResearchAgent",
        "quick_tasks": [
            "Produce a full competitor analysis: OpenMRS vs OPES Health Systems",
            "Research the healthcare digital landscape in Gabon — opportunity for OPES expansion",
            "Produce a weekly intelligence report for the CEMAC digital health market",
            "Identify all active WHO, World Bank, and USAID digital health projects in CEMAC 2024-2026",
            "Analyse the Cameroon Ministry of Health Digital Health Strategy 2026-2030 and OPES alignment",
        ]
    },
    "8": {
        "name": "NOVA",
        "role": "Business Intelligence",
        "emoji": "📊",
        "class": "NovaAnalyticsAgent",
        "quick_tasks": [
            "Build the complete KPI framework for all 8 AI employees at OPES Health Systems",
            "Design the weekly CEO dashboard template for OPES Health Systems",
            "Build a 90-day sales forecast model for OPES entering the Gabon market",
            "Design the lead funnel analytics framework: from LinkedIn outreach to signed contract",
            "Produce a market sizing analysis: total addressable market for OPES in CEMAC",
        ]
    },
}


def show_menu():
    table = Table(title="OPES Health Systems — AI Employee Team", border_style="green")
    table.add_column("#", style="bold cyan", width=3)
    table.add_column("Agent", style="bold white")
    table.add_column("Role", style="dim")
    for key, agent in AGENTS.items():
        table.add_row(key, f"{agent['emoji']} {agent['name']}", agent['role'])
    console.print(table)


def run_agent(agent_key: str, custom_task: str = ""):
    agent_info = AGENTS[agent_key]

    # Import and instantiate
    module = __import__(
        f"agents.{agent_info['class'].lower().replace('agent', '_agent').replace('__', '_')}",
        fromlist=[agent_info['class']]
    )

    # Map class names to module filenames
    class_to_module = {
        "AmaraSocialAgent":    "agents.amara_social",
        "ChisomServiceAgent":  "agents.chisom_service",
        "KofiMarketingAgent":  "agents.kofi_marketing",
        "ZaraContentAgent":    "agents.zara_content",
        "EmekaLeadsAgent":     "agents.emeka_leads",
        "FatimaOutreachAgent": "agents.fatima_outreach",
        "AtlasResearchAgent":  "agents.atlas_research",
        "NovaAnalyticsAgent":  "agents.nova_analytics",
    }

    import importlib
    mod = importlib.import_module(class_to_module[agent_info['class']])
    AgentClass = getattr(mod, agent_info['class'])
    agent = AgentClass()

    # Choose task
    if custom_task:
        task = custom_task
    else:
        console.print(f"\n[bold]Quick tasks for {agent_info['emoji']} {agent_info['name']}:[/bold]")
        for i, t in enumerate(agent_info['quick_tasks'], 1):
            console.print(f"  [cyan]{i}[/cyan]. {t}")
        console.print(f"  [cyan]0[/cyan]. Enter a custom task")

        choice = Prompt.ask("\nChoose", choices=["0","1","2","3","4","5"], default="1")
        if choice == "0":
            task = Prompt.ask("Enter your task")
        else:
            task = agent_info['quick_tasks'][int(choice) - 1]

    console.print(f"\n[dim]Running: {task}[/dim]\n")

    with console.status(f"[green]{agent_info['name']} is working...[/green]", spinner="dots"):
        result = agent.run_task(task)

    filepath = save_output(agent_info['name'], task, result)
    console.print(f"\n[green]✓ Saved to:[/green] [bold]{filepath}[/bold]")
    return result


def main():
    check_api_key()

    console.print(Panel(
        "[bold green]OPES Health Systems — AI Employee Team[/bold green]\n"
        "Phase 1: Manual operation — pick an agent, give a task, get real output.",
        border_style="green"
    ))

    while True:
        show_menu()
        console.print("  [cyan]0[/cyan]. Exit")
        choice = Prompt.ask("\nWhich agent", choices=["0","1","2","3","4","5","6","7","8"], default="1")

        if choice == "0":
            console.print("[dim]Goodbye.[/dim]")
            break

        run_agent(choice)

        again = Prompt.ask("\n[bold]Run another task?[/bold]", choices=["y","n"], default="y")
        if again == "n":
            break


if __name__ == "__main__":
    main()
