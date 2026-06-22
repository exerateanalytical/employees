"""
PromptEvaluator — scores agent output quality using Claude as the judge.

Scoring dimensions (each 0–20, total 0–100):
  1. OPES Specificity   — uses real product names, prices, CEMAC context
  2. Actionability      — output can be used immediately without edits
  3. Strategic Depth    — applies Hormozi/Gerber frameworks correctly
  4. Bilingual Quality  — appropriate EN/FR coverage for the task
  5. Professional Tone  — matches OPES brand voice, Africa-first perspective
"""

from __future__ import annotations

import os
import re

import anthropic

JUDGE_SYSTEM = """You are an expert quality evaluator for AI-generated business content.
You score outputs created by AI employees of Opes Health Systems, a Cameroonian digital health
company selling on-premise healthcare software across CEMAC and Africa.

You are strict, fair, and specific. You always explain your scores briefly."""

SCORING_TEMPLATE = """\
## TASK THE AI AGENT WAS GIVEN
{task}

## OUTPUT PRODUCED BY THE AGENT
{output}

## SCORING INSTRUCTIONS
Score the output on 5 dimensions. Each is worth 0–20 points. Be strict.

**1. OPES Specificity (0–20)**
Does the output reference actual OPES products (EMR, HIS, PHARMIS, CDMS, OPESCare, Triage, etc.),
real FCFA pricing, CEMAC geography (Cameroon, Gabon, etc.), or specific African healthcare pain points?
Generic content about "health software" that could apply to any company scores ≤5.

**2. Actionability (0–20)**
Can this output be used immediately without edits? Does it include complete copy, specific steps,
real subject lines, actual post captions, concrete numbers? Vague outlines score ≤5.

**3. Strategic Framework Application (0–20)**
Does it correctly apply Hormozi ($100M Offers/Leads), Gerber (E-Myth), or Fastlane principles?
Generic "best practices" marketing advice without these frameworks scores ≤8.

**4. Bilingual Quality (0–20)**
Where the task requires French or bilingual output, is the French accurate and idiomatic
(not machine-translated), culturally appropriate for CEMAC? If bilingual was not required,
score 20 automatically.

**5. Professional Excellence (0–20)**
Does this match the output quality of a senior professional in this role at an African tech company?
Would the CEO be proud to send this to a hospital director in Douala?

## RESPONSE FORMAT (strictly JSON)
{{
  "opes_specificity": <0-20>,
  "actionability": <0-20>,
  "strategic_framework": <0-20>,
  "bilingual_quality": <0-20>,
  "professional_excellence": <0-20>,
  "total": <0-100>,
  "reasoning": "<2-3 sentences explaining the main strengths and the single biggest weakness>"
}}"""


class PromptEvaluator:
    def __init__(self) -> None:
        self.client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    def score(self, task: str, output: str) -> dict:
        """Score an agent output. Returns dict with dimension scores and reasoning."""
        prompt = SCORING_TEMPLATE.format(task=task, output=output[:3000])
        response = self.client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=512,
            system=JUDGE_SYSTEM,
            messages=[{"role": "user", "content": prompt}],
        )
        raw = response.content[0].text.strip()
        # Extract JSON even if wrapped in markdown
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if match:
            import json
            return json.loads(match.group())
        # Fallback if JSON extraction fails
        return {
            "opes_specificity": 10,
            "actionability": 10,
            "strategic_framework": 10,
            "bilingual_quality": 10,
            "professional_excellence": 10,
            "total": 50,
            "reasoning": "Score parsing failed — defaulted to 50.",
        }
