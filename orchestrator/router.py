"""
WorkflowRouter — given a natural language description of a goal,
uses Claude to decide which workflow best matches and runs it.

This makes the system conversational: you describe what you want,
the router picks the right multi-agent workflow and fills in the parameters.
"""

from __future__ import annotations

import json
import os
import re

import anthropic

from .workflows import WORKFLOWS, build_workflow

ROUTER_SYSTEM = """You are the orchestrator for Opes Health Systems' AI employee team.
You receive a natural language goal and must decide which workflow to run and what parameters to extract.

Available workflows:
{workflow_list}

Respond ONLY with a JSON object:
{{
  "workflow_id": "<workflow_id from list above>",
  "parameters": {{
    "<param_name>": "<extracted value>",
    ...
  }},
  "reasoning": "<one sentence explaining why this workflow fits>"
}}

If no workflow fits well, use "custom" as the workflow_id and put the full goal in parameters.goal."""


class WorkflowRouter:
    def __init__(self) -> None:
        self.client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    def route(self, goal: str, verbose: bool = True) -> dict:
        """
        Parse a natural language goal, select the right workflow, run it.
        Returns the pipeline context dict.
        """
        workflow_list = "\n".join(
            f"- {wid}: {meta['description']} | params: {list(meta['params'].keys())}"
            for wid, meta in WORKFLOWS.items()
        )

        system = ROUTER_SYSTEM.format(workflow_list=workflow_list)

        response = self.client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=512,
            system=system,
            messages=[{"role": "user", "content": f"Goal: {goal}"}],
        )
        raw = response.content[0].text.strip()
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if not match:
            raise ValueError(f"Router failed to produce valid JSON: {raw}")

        decision = json.loads(match.group())
        workflow_id = decision.get("workflow_id", "custom")
        params = decision.get("parameters", {})
        reasoning = decision.get("reasoning", "")

        if verbose:
            from rich.console import Console
            Console().print(
                f"[dim]Router → [bold]{workflow_id}[/bold] | {reasoning}[/dim]"
            )

        if workflow_id not in WORKFLOWS and workflow_id != "custom":
            workflow_id = "custom"
            params = {"goal": goal}

        pipeline = build_workflow(workflow_id, params)
        return pipeline.run(params, verbose=verbose)
