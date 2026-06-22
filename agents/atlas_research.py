"""
ATLAS — Web Research & Competitor Intelligence
Monitors competitors, markets, tenders, and opportunities across Africa.
"""

from __future__ import annotations

from .base_agent import BaseAgent


class AtlasResearchAgent(BaseAgent):
    name = "ATLAS"
    role = "Web Research & Competitor Intelligence"
    emoji = "🌍"
    prompt_file = "atlas_research.md"

    def analyze_competitor(self, competitor_name: str, website: str, context: str = "") -> str:
        return self.run_task(
            f"Perform a comprehensive competitor analysis:\n"
            f"Competitor: {competitor_name}\n"
            f"Website: {website}\n"
            f"Additional context: {context}\n\n"
            f"Use the Competitor Analysis Template from your prompt. "
            f"Identify their products, pricing, geographic focus, marketing strategy, "
            f"strengths, weaknesses, and specific opportunities for Opes."
        )

    def produce_weekly_intel_report(self, competitor_updates: str = "", market_news: str = "") -> str:
        return self.run_task(
            f"Produce the weekly ATLAS Intelligence Report.\n"
            f"Competitor updates to incorporate: {competitor_updates or 'None provided — generate research agenda'}\n"
            f"Market news to incorporate: {market_news or 'None provided — generate monitoring checklist'}\n\n"
            f"Follow the Weekly Intelligence Report format exactly. "
            f"Include: urgent items, competitor updates, market opportunities, "
            f"SEO intel, social listening highlights, country spotlight, and recommended actions."
        )

    def research_country_market(self, country: str) -> str:
        return self.run_task(
            f"Produce a detailed Country Market Intelligence Report for: {country}\n\n"
            f"Follow the Country Market Deep Dive template from your prompt. "
            f"Cover: healthcare system overview, key institutions, regulatory environment, "
            f"market opportunity for Opes, and contacts to identify."
        )

    def find_tenders(self, product_category: str, region: str) -> str:
        return self.run_task(
            f"Identify and format tender/procurement alerts for:\n"
            f"Product category: {product_category}\n"
            f"Region: {region}\n\n"
            f"List all sources to monitor, search terms to use, "
            f"and format findings using the Tender Alert Template. "
            f"Prioritize by deadline and value."
        )

    def research_industry_trends(self, topic: str) -> str:
        return self.run_task(
            f"Research current trends in: {topic}\n"
            f"Focus: African healthcare market specifically.\n\n"
            f"Identify: top 5 trends, implications for Opes Health Systems, "
            f"opportunities to act on, and threats to watch."
        )

    def social_listening_report(self, keywords: list[str]) -> str:
        kw_str = ", ".join(keywords)
        return self.run_task(
            f"Perform social listening analysis for these keywords:\n"
            f"{kw_str}\n\n"
            f"Identify: what people are saying, pain points being expressed, "
            f"competitor mentions, lead opportunities, content ideas, "
            f"and any threats or crises to monitor."
        )

    def build_competitor_monitoring_plan(self) -> str:
        return self.run_task(
            f"Build a comprehensive competitor monitoring plan for Opes Health Systems.\n\n"
            f"Based on the company context, identify:\n"
            f"1. Who our main competitors likely are in the African healthcare space\n"
            f"2. What tools to use for monitoring\n"
            f"3. What to monitor and how often\n"
            f"4. How to report findings\n"
            f"5. Alert triggers that require immediate action"
        )
