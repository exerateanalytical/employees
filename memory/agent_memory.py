"""
AgentMemory — the memory interface every agent uses.

Four memory types per Hermes-style architecture:
  - episodic:   what happened (interactions, tasks completed)
  - semantic:   what was learned (insights, facts, patterns)
  - procedural: what worked (successful approaches, winning content/sequences)
  - entity:     who exists (customers, leads, competitors, contacts)
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from .vector_store import VectorStore


class AgentMemory:
    def __init__(self, agent_name: str) -> None:
        self.agent_name = agent_name
        self.store = VectorStore(agent_name)

    # ── Store ────────────────────────────────────────────────────────────────

    def remember_interaction(self, task: str, result_summary: str, outcome: str = "") -> str:
        """Store what happened in a session."""
        text = (
            f"TASK: {task}\n"
            f"RESULT SUMMARY: {result_summary}\n"
            f"OUTCOME: {outcome}"
        )
        return self.store.store(text, "episodic", {
            "date": datetime.utcnow().isoformat(),
            "task": task[:200],
            "outcome": outcome,
        })

    def learn(self, insight: str, source: str = "", confidence: str = "medium") -> str:
        """Store a learned insight or pattern."""
        return self.store.store(insight, "semantic", {
            "date": datetime.utcnow().isoformat(),
            "source": source,
            "confidence": confidence,
        })

    def remember_success(self, approach: str, result: str, context: str = "") -> str:
        """Store a winning approach — content that worked, sequence that converted, etc."""
        text = f"APPROACH: {approach}\nRESULT: {result}\nCONTEXT: {context}"
        return self.store.store(text, "procedural", {
            "date": datetime.utcnow().isoformat(),
            "context": context[:200],
        })

    def remember_entity(
        self,
        entity_type: str,
        name: str,
        details: str,
        extra: dict[str, Any] | None = None,
    ) -> str:
        """Store a person, company, competitor, or contact."""
        text = f"TYPE: {entity_type}\nNAME: {name}\nDETAILS: {details}"
        meta = {"entity_type": entity_type, "name": name, "date": datetime.utcnow().isoformat()}
        if extra:
            meta.update(extra)
        return self.store.store(text, "entity", meta)

    # ── Retrieve ─────────────────────────────────────────────────────────────

    def recall(self, query: str, n: int = 5) -> str:
        """
        Retrieve memories relevant to a query.
        Returns a formatted string ready to inject into a prompt.
        """
        memories = self.store.retrieve(query, n=n)
        if not memories:
            return ""
        lines = [f"## Relevant memories for: '{query}'\n"]
        for m in memories:
            mtype = m["metadata"].get("memory_type", "?")
            date = m["metadata"].get("date", "")[:10]
            lines.append(f"[{mtype.upper()} | {date} | relevance {m['relevance']}]")
            lines.append(m["text"])
            lines.append("")
        return "\n".join(lines)

    def recall_entities(self, query: str, n: int = 5) -> str:
        memories = self.store.retrieve(query, n=n, memory_type="entity")
        if not memories:
            return ""
        lines = ["## Known entities:\n"]
        for m in memories:
            lines.append(m["text"])
            lines.append("")
        return "\n".join(lines)

    def recall_what_worked(self, context: str, n: int = 3) -> str:
        memories = self.store.retrieve(context, n=n, memory_type="procedural")
        if not memories:
            return ""
        lines = ["## What has worked before:\n"]
        for m in memories:
            lines.append(m["text"])
            lines.append("")
        return "\n".join(lines)

    def recent_history(self, n: int = 5) -> str:
        memories = self.store.get_recent(n=n, memory_type="episodic")
        if not memories:
            return ""
        lines = [f"## {self.agent_name}'s recent activity:\n"]
        for m in memories:
            date = m["metadata"].get("date", "")[:10]
            task = m["metadata"].get("task", "")
            lines.append(f"[{date}] {task}")
        return "\n".join(lines)

    # ── Stats ────────────────────────────────────────────────────────────────

    def stats(self) -> dict:
        return self.store.stats()
