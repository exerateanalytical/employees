"""
CHISOM — Customer Service Representative
Handles all customer inquiries with speed, empathy, and resolution focus.
"""

from __future__ import annotations

from .base_agent import BaseAgent


class ChisomServiceAgent(BaseAgent):
    name = "CHISOM"
    role = "Customer Service Representative"
    emoji = "💬"
    prompt_file = "chisom_service.md"

    def handle_inquiry(self, message: str, customer_name: str = "", channel: str = "email") -> str:
        context = f"Customer name: {customer_name}\n" if customer_name else ""
        return self.run_task(
            f"{context}Channel: {channel}\n"
            f"Customer message: {message}\n\n"
            f"Respond as CHISOM. Be warm, direct, and resolve or escalate appropriately. "
            f"Detect the language and respond in the same language."
        )

    def handle_complaint(self, complaint: str, customer_name: str, product: str = "") -> str:
        product_note = f" about product: {product}" if product else ""
        return self.run_task(
            f"Customer {customer_name} has a complaint{product_note}:\n"
            f"'{complaint}'\n\n"
            f"Use the complaint response protocol: empathy first, acknowledge, investigate, "
            f"resolve with clear timeline, and follow up commitment."
        )

    def write_faq(self, product_or_topic: str) -> str:
        return self.run_task(
            f"Write 10 frequently asked questions and answers about: {product_or_topic}\n"
            f"Make them specific to our African healthcare market context. "
            f"Produce in both English and French."
        )

    def draft_escalation(self, issue: str, customer: str, escalate_to: str) -> str:
        return self.run_task(
            f"Draft an internal escalation message for this issue:\n"
            f"Customer: {customer}\n"
            f"Issue: {issue}\n"
            f"Escalate to: {escalate_to}\n"
            f"Include: urgency level, customer history summary, recommended resolution."
        )

    def collect_testimonial_request(self, customer_name: str, product: str) -> str:
        return self.run_task(
            f"Write a polite testimonial request to {customer_name} who purchased {product}.\n"
            f"Make it feel personal and low-pressure. Include EN + FR versions."
        )

    def record_resolved_case(self, customer_name: str, issue: str, resolution: str) -> None:
        """Store a resolved case so CHISOM learns effective resolutions over time."""
        self.remember_success(
            approach=f"Resolution for: {issue}",
            result=f"Resolved for {customer_name}",
            context=resolution,
        )

    def remember_customer(self, name: str, company: str, product: str, notes: str) -> None:
        """Store a customer profile for future personalised support."""
        self.remember_entity(
            entity_type="customer",
            name=f"{name} ({company})",
            details=f"Product: {product}. Notes: {notes}",
        )
