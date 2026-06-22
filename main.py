"""
Opes Health Systems — AI Employees Entry Point

Usage:
  # Start the API server (all 8 agents + scheduler):
  python main.py server

  # Run a specific agent task interactively:
  python main.py run amara "Create a Facebook post about malaria prevention"
  python main.py run chisom "A customer from Nigeria is asking about delivery times"
  python main.py run kofi "Build a campaign for our new product"
  python main.py run zara "Write a blog about healthcare in West Africa"
  python main.py run emeka "Find 20 hospital leads in Kenya"
  python main.py run fatima "Onboard Dr. Bello from Lagos General Hospital"
  python main.py run atlas "Analyze competitor MedAfrica"
  python main.py run nova "Produce weekly CEO report"

  # Run the scheduler in foreground (for testing):
  python main.py scheduler

  # Phase 3: evolve agent prompts (Darwin Gödel Machine):
  python main.py evolve                # evolve all 8 agents
  python main.py evolve amara kofi     # evolve specific agents
  python main.py evolve --status       # show evolution history
"""

from __future__ import annotations

import sys
import time

from dotenv import load_dotenv

load_dotenv()


def run_server():
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=False)


def run_agent(agent_name: str, task: str):
    from agents import (
        AmaraSocialAgent,
        AtlasResearchAgent,
        ChisomServiceAgent,
        EmekaLeadsAgent,
        FatimaOutreachAgent,
        KofiMarketingAgent,
        NovaAnalyticsAgent,
        ZaraContentAgent,
    )

    agents = {
        "amara": AmaraSocialAgent,
        "chisom": ChisomServiceAgent,
        "kofi": KofiMarketingAgent,
        "zara": ZaraContentAgent,
        "emeka": EmekaLeadsAgent,
        "fatima": FatimaOutreachAgent,
        "atlas": AtlasResearchAgent,
        "nova": NovaAnalyticsAgent,
    }

    name = agent_name.lower()
    if name not in agents:
        print(f"Unknown agent: {agent_name}. Choose from: {', '.join(agents)}")
        sys.exit(1)

    agent = agents[name]()
    agent.run_task(task)


def run_scheduler():
    from scheduler import build_scheduler
    scheduler = build_scheduler()
    scheduler.start()
    print("Scheduler running. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        scheduler.shutdown()
        print("Scheduler stopped.")


def show_help():
    print(__doc__)


if __name__ == "__main__":
    args = sys.argv[1:]

    if not args or args[0] in ("-h", "--help", "help"):
        show_help()
    elif args[0] == "server":
        run_server()
    elif args[0] == "scheduler":
        run_scheduler()
    elif args[0] == "run" and len(args) >= 3:
        run_agent(args[1], " ".join(args[2:]))
    elif args[0] == "evolve":
        import subprocess
        subprocess.run([sys.executable, "self_improve.py"] + args[1:])
    else:
        show_help()
