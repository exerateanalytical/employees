"""
Tracks every prompt version, its score, and whether it was adopted.
Persists to a JSON file so the evolutionary history survives restarts.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

STORE_PATH = Path(__file__).parent.parent / "evolution_log.json"


class EvolutionStore:
    def __init__(self) -> None:
        self._data: dict[str, Any] = self._load()

    def _load(self) -> dict:
        if STORE_PATH.exists():
            return json.loads(STORE_PATH.read_text())
        return {"generations": [], "current_champions": {}}

    def _save(self) -> None:
        STORE_PATH.write_text(json.dumps(self._data, indent=2, ensure_ascii=False))

    # ── Write ────────────────────────────────────────────────────────────────

    def record_generation(
        self,
        agent: str,
        generation: int,
        task: str,
        original_score: float,
        mutant_score: float,
        winner: str,          # "original" | "mutant"
        mutation_summary: str,
        original_prompt_hash: str,
        mutant_prompt_hash: str,
    ) -> None:
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "agent": agent,
            "generation": generation,
            "task": task[:200],
            "original_score": original_score,
            "mutant_score": mutant_score,
            "winner": winner,
            "improvement": round(mutant_score - original_score, 2),
            "mutation_summary": mutation_summary,
            "original_hash": original_prompt_hash,
            "mutant_hash": mutant_prompt_hash,
            "adopted": winner == "mutant",
        }
        self._data["generations"].append(entry)
        if winner == "mutant":
            self._data["current_champions"][agent] = {
                "generation": generation,
                "score": mutant_score,
                "adopted_at": entry["timestamp"],
            }
        self._save()

    # ── Read ─────────────────────────────────────────────────────────────────

    def agent_history(self, agent: str) -> list[dict]:
        return [g for g in self._data["generations"] if g["agent"] == agent]

    def champion(self, agent: str) -> dict | None:
        return self._data["current_champions"].get(agent)

    def total_generations(self) -> int:
        return len(self._data["generations"])

    def adoption_rate(self) -> float:
        gens = self._data["generations"]
        if not gens:
            return 0.0
        adopted = sum(1 for g in gens if g["adopted"])
        return round(adopted / len(gens), 3)

    def summary(self) -> dict:
        gens = self._data["generations"]
        by_agent: dict[str, dict] = {}
        for g in gens:
            a = g["agent"]
            if a not in by_agent:
                by_agent[a] = {"generations": 0, "adopted": 0, "avg_improvement": []}
            by_agent[a]["generations"] += 1
            if g["adopted"]:
                by_agent[a]["adopted"] += 1
            by_agent[a]["avg_improvement"].append(g["improvement"])
        for a, v in by_agent.items():
            improvements = v.pop("avg_improvement")
            v["avg_improvement"] = round(sum(improvements) / len(improvements), 2) if improvements else 0
        return {
            "total_generations": len(gens),
            "adoption_rate": self.adoption_rate(),
            "by_agent": by_agent,
            "champions": self._data["current_champions"],
        }
