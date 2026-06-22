"""
PromptEvolver — the mutation engine.

Given the current system prompt for an agent and the evaluator's diagnosis,
this generates an improved prompt variant. The mutation is targeted:
it reads the scoring breakdown and specifically strengthens whatever
dimension scored lowest.

This is the Darwin Gödel Machine in practice:
  current prompt → evaluate → diagnose weakness → targeted mutation → re-evaluate → keep winner
"""

from __future__ import annotations

import os

import anthropic

EVOLVER_SYSTEM = """You are a master prompt engineer specialising in AI agent design for African B2B tech companies.

You will be given:
1. An existing system prompt for an AI employee at Opes Health Systems
2. A quality score breakdown showing where the agent's output is weakest
3. An example task and output that illustrates the weakness

Your job is to improve the system prompt to fix the weakest dimension WITHOUT breaking what is working.

Rules:
- Never remove product knowledge, pricing, or company context
- Never make the prompt generic — it must remain deeply OPES-specific
- Keep all CEMAC/African healthcare context
- If the weakness is strategic frameworks, add more specific Hormozi/Gerber instructions
- If the weakness is bilingual quality, add French writing guidelines and examples
- If the weakness is actionability, add more explicit output format templates
- If the weakness is OPES specificity, embed more product names, prices, use cases
- Output ONLY the improved prompt. No explanation, no preamble, no meta-commentary."""

MUTATION_TEMPLATE = """\
## CURRENT SYSTEM PROMPT
{current_prompt}

## QUALITY SCORE BREAKDOWN
Total: {total}/100

Dimension scores:
- OPES Specificity: {opes_specificity}/20
- Actionability: {actionability}/20
- Strategic Framework: {strategic_framework}/20
- Bilingual Quality: {bilingual_quality}/20
- Professional Excellence: {professional_excellence}/20

Evaluator reasoning: {reasoning}

## WEAKEST DIMENSION TO FIX
{weakest_dimension}: {weakest_score}/20

## EXAMPLE TASK AND OUTPUT THAT ILLUSTRATED THE WEAKNESS
Task: {task}
Output (first 800 chars): {output_excerpt}

## YOUR JOB
Rewrite the system prompt to specifically improve the {weakest_dimension} dimension.
Focus your changes on the section(s) most responsible for this weakness.
Keep everything else intact. Output only the improved prompt."""


def _find_weakest(scores: dict) -> tuple[str, int]:
    dims = {
        "OPES Specificity": scores.get("opes_specificity", 10),
        "Actionability": scores.get("actionability", 10),
        "Strategic Framework": scores.get("strategic_framework", 10),
        "Bilingual Quality": scores.get("bilingual_quality", 10),
        "Professional Excellence": scores.get("professional_excellence", 10),
    }
    weakest = min(dims, key=lambda k: dims[k])
    return weakest, dims[weakest]


class PromptEvolver:
    def __init__(self) -> None:
        self.client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    def mutate(
        self,
        current_prompt: str,
        scores: dict,
        task: str,
        output: str,
    ) -> tuple[str, str, str]:
        """
        Generate a mutant prompt targeting the weakest scoring dimension.

        Returns:
            (mutant_prompt, weakest_dimension, mutation_summary)
        """
        weakest_dim, weakest_score = _find_weakest(scores)

        prompt = MUTATION_TEMPLATE.format(
            current_prompt=current_prompt,
            total=scores.get("total", 50),
            opes_specificity=scores.get("opes_specificity", 10),
            actionability=scores.get("actionability", 10),
            strategic_framework=scores.get("strategic_framework", 10),
            bilingual_quality=scores.get("bilingual_quality", 10),
            professional_excellence=scores.get("professional_excellence", 10),
            reasoning=scores.get("reasoning", ""),
            weakest_dimension=weakest_dim,
            weakest_score=weakest_score,
            task=task[:300],
            output_excerpt=output[:800],
        )

        response = self.client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4096,
            system=EVOLVER_SYSTEM,
            messages=[{"role": "user", "content": prompt}],
        )
        mutant_prompt = response.content[0].text.strip()
        mutation_summary = f"Targeted improvement: {weakest_dim} (was {weakest_score}/20)"
        return mutant_prompt, weakest_dim, mutation_summary
