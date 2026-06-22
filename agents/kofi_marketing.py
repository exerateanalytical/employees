"""
KOFI — Marketing Strategist
Builds campaigns, email sequences, ad copy, and lead magnet strategies.
"""

from __future__ import annotations

from .base_agent import BaseAgent


class KofiMarketingAgent(BaseAgent):
    name = "KOFI"
    role = "Marketing Strategist"
    emoji = "🎯"
    prompt_file = "kofi_marketing.md"

    def build_campaign(self, product: str, goal: str, budget: str, duration: str) -> str:
        return self.run_task(
            f"Build a complete marketing campaign brief:\n"
            f"Product: {product}\n"
            f"Goal: {goal}\n"
            f"Budget: {budget}\n"
            f"Duration: {duration}\n\n"
            f"Use the Grand Slam Offer framework. Include channels, messaging, "
            f"value stack, CTA, KPIs, and budget allocation."
        )

    def write_email_sequence(self, icp: str, product: str, sequence_type: str = "welcome") -> str:
        return self.run_task(
            f"Write a complete {sequence_type} email sequence for:\n"
            f"ICP: {icp}\n"
            f"Product/Service: {product}\n\n"
            f"Apply Hormozi's email sequence framework. "
            f"Include: subject lines (5 options each), preview text, full body, and CTA. "
            f"Write in English. Flag which emails need French versions."
        )

    def write_ad_copy(self, platform: str, product: str, icp: str) -> str:
        return self.run_task(
            f"Write {platform} ad copy for:\n"
            f"Product: {product}\n"
            f"Target ICP: {icp}\n\n"
            f"Use the Hook-Problem-Solution-Proof-Offer-CTA formula. "
            f"Provide: headline (5 options), primary text (3 variations), description, CTA. "
            f"Include EN + FR versions."
        )

    def create_lead_magnet(self, icp: str) -> str:
        return self.run_task(
            f"Design a lead magnet strategy for ICP: {icp}\n\n"
            f"Include:\n"
            f"1. Lead magnet concept and title (3 options)\n"
            f"2. Full outline of the lead magnet content\n"
            f"3. How to deliver it\n"
            f"4. The opt-in page copy (EN + FR)\n"
            f"5. Thank-you page copy\n"
            f"6. Follow-up email (24 hours after download)"
        )

    def analyze_funnel(self, funnel_data: dict) -> str:
        import json
        return self.run_task(
            f"Analyze this marketing funnel performance and diagnose problems:\n"
            f"{json.dumps(funnel_data, indent=2)}\n\n"
            f"Identify the biggest bottleneck. Recommend exactly what to change and why. "
            f"Prioritize by potential impact."
        )

    def write_seo_strategy(self, country: str, product_category: str) -> str:
        return self.run_task(
            f"Build a 90-day SEO strategy for:\n"
            f"Target country/region: {country}\n"
            f"Product category: {product_category}\n\n"
            f"Include: keyword research direction, content plan, on-page checklist, "
            f"link-building strategy relevant to African web ecosystem."
        )

    def record_winning_campaign(self, campaign_name: str, result: str, approach: str) -> None:
        """Store a campaign that exceeded targets so KOFI can replicate it."""
        self.remember_success(approach=f"Campaign: {campaign_name}. {approach}", result=result)

    def learn_market_insight(self, insight: str) -> None:
        """Store a marketing insight about the African healthcare audience."""
        self.learn(insight, source="KOFI campaign data")
