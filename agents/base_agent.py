"""
Base agent class — all 8 Opes AI employees inherit from this.
"""

from __future__ import annotations

import os
import yaml
from pathlib import Path
from typing import Any

import anthropic
from rich.console import Console
from rich.panel import Panel

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

    Each agent has:
    - A name, role, and emoji identifier
    - Full company context from config/company.yaml
    - A rich system prompt from config/prompts/<prompt_file>
    - A conversation history (per-session)
    - Access to the Claude API
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

    def _build_system_prompt(self) -> str:
        prompt_path = PROMPTS_DIR / self.prompt_file
        agent_prompt = prompt_path.read_text()

        company_yaml = yaml.dump(self.company, allow_unicode=True, sort_keys=False)
        company_context = f"""
---
## COMPANY KNOWLEDGE BASE (from config/company.yaml)

```yaml
{company_yaml}
```

Use this company data in every response. Know the products, markets, ICPs,
brand voice, and offer framework as if you built the company yourself.
---
"""
        return agent_prompt + company_context

    def think(
        self,
        message: str,
        tools: list[dict] | None = None,
        stream: bool = False,
    ) -> str:
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

        # Handle tool use or plain text response
        reply_parts = []
        for block in response.content:
            if block.type == "text":
                reply_parts.append(block.text)

        reply = "\n".join(reply_parts).strip()
        self.history.append({"role": "assistant", "content": response.content})
        return reply

    def reset(self) -> None:
        self.history = []

    def display(self, message: str) -> None:
        console.print(
            Panel(
                message,
                title=f"{self.emoji} {self.name} | {self.role}",
                border_style="green",
            )
        )

    def run_task(self, task: str) -> str:
        """Entry point for scheduled or on-demand tasks."""
        self.reset()
        result = self.think(task)
        self.display(result)
        return result
