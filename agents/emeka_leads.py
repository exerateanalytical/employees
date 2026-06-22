"""
EMEKA — Lead Generation Specialist
Finds, qualifies, and nurtures prospects across Africa.
"""

from __future__ import annotations

from .base_agent import BaseAgent


class EmekaLeadsAgent(BaseAgent):
    name = "EMEKA"
    role = "Lead Generation Specialist"
    emoji = "🔍"
    prompt_file = "emeka_leads.md"

    def research_prospects(self, segment: str, country: str, count: int = 20) -> str:
        return self.run_task(
            f"Research and list {count} qualified prospects for Opes Health Systems:\n"
            f"Segment: {segment}\n"
            f"Country: {country}\n\n"
            f"For each prospect list: Organization name, type, size estimate, "
            f"relevant contact title, LinkedIn/website URL if known, and tier (A/B/C). "
            f"Focus on decision-makers who control procurement."
        )

    def write_outreach_sequence(self, segment: str, country: str, product: str) -> str:
        return self.run_task(
            f"Write a complete cold outreach sequence:\n"
            f"Target segment: {segment}\n"
            f"Country: {country}\n"
            f"Product to position: {product}\n\n"
            f"Include: 4-email sequence (day 0, 3, 7, 14) + LinkedIn sequence. "
            f"Each email: subject line, preview, full body, CTA. "
            f"Use Hormozi value-first approach — no immediate pitch."
        )

    def qualify_lead(self, company: str, contact: str, context: str) -> str:
        return self.run_task(
            f"Qualify this lead using BANT framework:\n"
            f"Company: {company}\n"
            f"Contact: {contact}\n"
            f"Context known: {context}\n\n"
            f"Generate: qualification questions to ask, lead tier (A/B/C) based on available info, "
            f"recommended next action, and any red flags."
        )

    def find_tenders(self, product_category: str, region: str) -> str:
        return self.run_task(
            f"Identify all active procurement opportunities and tenders for:\n"
            f"Product category: {product_category}\n"
            f"Region: {region}\n\n"
            f"List the most likely sources to check, what to search for, "
            f"and provide a tender monitoring plan for this category. "
            f"Format as actionable intelligence with links/sources."
        )

    def write_linkedin_connection_campaign(self, icp: str, country: str) -> str:
        return self.run_task(
            f"Write a LinkedIn connection + nurture campaign targeting:\n"
            f"ICP: {icp}\n"
            f"Country: {country}\n\n"
            f"Include: connection request note, day-3 message, day-10 message, "
            f"day-20 meeting request. Keep each under 300 characters for connection note "
            f"and under 500 words for follow-up messages. Be genuine, not salesy."
        )

    def produce_weekly_lead_report(self, data: dict) -> str:
        import json
        return self.run_task(
            f"Produce the weekly lead generation report based on this data:\n"
            f"{json.dumps(data, indent=2)}\n\n"
            f"Include: leads by tier, sources performance, outreach metrics, "
            f"hot leads ready for handoff, and next week's prospecting priorities."
        )

    def store_lead(self, name: str, company: str, country: str, tier: str, notes: str) -> None:
        """Store a qualified lead in memory so EMEKA remembers them across sessions."""
        self.remember_entity(
            entity_type="lead",
            name=f"{name} — {company} ({country})",
            details=f"Tier: {tier}. {notes}",
        )

    def record_winning_sequence(self, sequence_name: str, response_rate: str, context: str) -> None:
        """Store a cold outreach sequence that delivered strong results."""
        self.remember_success(
            approach=sequence_name,
            result=f"Response rate: {response_rate}",
            context=context,
        )
