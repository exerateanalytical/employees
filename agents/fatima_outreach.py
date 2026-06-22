"""
FATIMA — Customer Outreach & CRM Manager
Manages customer lifecycle, retention, re-engagement, and referrals.
"""

from __future__ import annotations

from .base_agent import BaseAgent


class FatimaOutreachAgent(BaseAgent):
    name = "FATIMA"
    role = "Customer Outreach & CRM Manager"
    emoji = "💛"
    prompt_file = "fatima_outreach.md"

    def onboard_customer(self, customer_name: str, company: str, product: str, country: str) -> str:
        return self.run_task(
            f"Create a 30-day onboarding sequence for a new customer:\n"
            f"Customer: {customer_name} at {company} ({country})\n"
            f"Product purchased: {product}\n\n"
            f"Include all touchpoints: Day 0, 3, 7, 14, 30. "
            f"For each: channel (WhatsApp/email), message content (EN + FR), goal. "
            f"Make each message feel genuinely personal."
        )

    def write_reengagement_campaign(self, segment: str, inactive_days: int) -> str:
        return self.run_task(
            f"Write a re-engagement campaign for customers inactive for {inactive_days}+ days:\n"
            f"Customer segment: {segment}\n\n"
            f"Include 3-email sequence + 1 WhatsApp message. "
            f"Be honest about noticing their absence. Provide real value. "
            f"End with a genuine offer if appropriate. EN + FR versions."
        )

    def write_winback_campaign(self, segment: str, product: str) -> str:
        return self.run_task(
            f"Write a win-back campaign for lapsed customers (6+ months no order):\n"
            f"Segment: {segment}\n"
            f"Key product: {product}\n\n"
            f"3-email sequence. Acknowledge the gap, show what's new, "
            f"make a compelling return offer, include urgency. EN + FR."
        )

    def request_referral(self, customer_name: str, company: str, product: str) -> str:
        return self.run_task(
            f"Write a referral request to a happy customer:\n"
            f"Customer: {customer_name} at {company}\n"
            f"Product they use: {product}\n\n"
            f"WhatsApp message + email version. Make it personal, low-pressure, "
            f"and offer a clear referral benefit. EN + FR."
        )

    def write_monthly_crm_plan(self, customer_segments: dict) -> str:
        import json
        return self.run_task(
            f"Create a monthly CRM outreach plan for these customer segments:\n"
            f"{json.dumps(customer_segments, indent=2)}\n\n"
            f"For each segment: touch frequency, channel mix, content theme, "
            f"upsell opportunities, and success metrics."
        )

    def draft_special_occasion_message(self, occasion: str, segment: str) -> str:
        return self.run_task(
            f"Write a special occasion message for {occasion}:\n"
            f"Customer segment: {segment}\n\n"
            f"WhatsApp message (under 150 words) + email version. "
            f"Warm and human — no hard sell. Bilingual EN/FR."
        )

    def write_upsell_sequence(self, current_product: str, target_product: str, segment: str) -> str:
        return self.run_task(
            f"Write a gentle upsell sequence:\n"
            f"Customers currently buying: {current_product}\n"
            f"Upsell to: {target_product}\n"
            f"Segment: {segment}\n\n"
            f"2-email sequence. Lead with how the upgrade serves them better. "
            f"Never feel pushy. Frame as a genuine recommendation. EN + FR."
        )

    def store_customer(self, name: str, company: str, country: str, product: str, notes: str) -> None:
        """Store a customer profile so FATIMA remembers them across outreach campaigns."""
        self.remember_entity(
            entity_type="customer",
            name=f"{name} — {company} ({country})",
            details=f"Product: {product}. {notes}",
        )

    def record_winning_outreach(self, campaign: str, open_rate: str, conversion: str) -> None:
        """Store an outreach campaign that achieved strong results."""
        self.remember_success(
            approach=campaign,
            result=f"Open rate: {open_rate}. Conversion: {conversion}",
        )
