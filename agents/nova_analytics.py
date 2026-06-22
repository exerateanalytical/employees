"""
NOVA — Business Intelligence Analyst
Transforms data into executive-ready reports and strategic recommendations.
"""

from __future__ import annotations

import json

from .base_agent import BaseAgent


class NovaAnalyticsAgent(BaseAgent):
    name = "NOVA"
    role = "Business Intelligence Analyst"
    emoji = "📊"
    prompt_file = "nova_analytics.md"

    def weekly_ceo_report(self, data: dict) -> str:
        return self.run_task(
            f"Produce the weekly CEO Dashboard Report:\n"
            f"{json.dumps(data, indent=2)}\n\n"
            f"Use the CEO Dashboard format. Start with TL;DR (3 bullets). "
            f"Include: revenue snapshot, top countries, top products, pipeline health, "
            f"alerts/watches/wins. End with 3 concrete recommendations for next week."
        )

    def ai_employee_performance_review(self, kpi_data: dict) -> str:
        return self.run_task(
            f"Produce a performance review for all AI employees based on their KPIs:\n"
            f"{json.dumps(kpi_data, indent=2)}\n\n"
            f"For each agent (AMARA, CHISOM, KOFI, ZARA, EMEKA, FATIMA, ATLAS): "
            f"score performance (1-5), identify what's working, what needs improvement, "
            f"and one specific recommendation to improve output next week."
        )

    def monthly_business_review(self, monthly_data: dict) -> str:
        return self.run_task(
            f"Produce the full Monthly Business Review:\n"
            f"{json.dumps(monthly_data, indent=2)}\n\n"
            f"Follow the Monthly Business Review format. Include: "
            f"executive summary, revenue analysis, customer cohort analysis, "
            f"AI employee performance, wins, misses, and next month priorities."
        )

    def funnel_analysis(self, funnel_data: dict) -> str:
        return self.run_task(
            f"Analyze this marketing/sales funnel and find the biggest leak:\n"
            f"{json.dumps(funnel_data, indent=2)}\n\n"
            f"Identify: conversion rate at each stage, where the most prospects are lost, "
            f"likely root cause, and specific recommendations to fix it."
        )

    def country_revenue_analysis(self, revenue_by_country: dict) -> str:
        return self.run_task(
            f"Analyze revenue performance by country:\n"
            f"{json.dumps(revenue_by_country, indent=2)}\n\n"
            f"Identify: top performers, underperformers, fastest growth markets, "
            f"markets with highest potential vs. current performance, "
            f"and recommended country-level strategy shifts."
        )

    def build_kpi_framework(self) -> str:
        return self.run_task(
            f"Build the complete KPI framework for Opes Health Systems.\n\n"
            f"For each business function (Sales, Marketing, Customer Service, "
            f"Social Media, Lead Gen, Retention, Research), define:\n"
            f"- Primary KPIs (3-5 per function)\n"
            f"- Target benchmarks (based on African healthcare B2B/B2C norms)\n"
            f"- Measurement frequency (daily/weekly/monthly)\n"
            f"- Data source\n"
            f"- Owner (which AI employee is responsible)\n"
            f"Format as a master dashboard specification."
        )

    def forecast_revenue(self, historical_data: dict, period: str = "next 90 days") -> str:
        return self.run_task(
            f"Produce a revenue forecast for {period}:\n"
            f"Historical data:\n{json.dumps(historical_data, indent=2)}\n\n"
            f"Include: base case, optimistic case, pessimistic case. "
            f"State your assumptions clearly. Identify the key variables that will "
            f"determine which scenario plays out."
        )
