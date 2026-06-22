"""
Email delivery via SendGrid.
Handles transactional emails, newsletters, and drip sequences.
"""

from __future__ import annotations

import os
from typing import Any

import sendgrid
from sendgrid.helpers.mail import Mail, To


class EmailTools:
    def __init__(self) -> None:
        self.client = sendgrid.SendGridAPIClient(api_key=os.environ["SENDGRID_API_KEY"])
        self.from_email = os.environ.get("FROM_EMAIL", "noreply@opeshealthsystems.com")
        self.from_name = os.environ.get("FROM_NAME", "Opes Health Systems")

    def send(
        self,
        to_email: str,
        subject: str,
        html_body: str,
        plain_body: str | None = None,
        reply_to: str | None = None,
    ) -> dict[str, Any]:
        message = Mail(
            from_email=(self.from_email, self.from_name),
            to_emails=to_email,
            subject=subject,
            html_content=html_body,
            plain_text_content=plain_body or "",
        )
        if reply_to:
            message.reply_to = reply_to

        response = self.client.send(message)
        return {
            "status_code": response.status_code,
            "message_id": response.headers.get("X-Message-Id"),
        }

    def send_bulk(
        self,
        recipients: list[dict],
        subject: str,
        html_template: str,
    ) -> list[dict]:
        """
        Send personalised bulk email.
        Each recipient dict: {"email": str, "name": str, "variables": dict}
        """
        results = []
        for r in recipients:
            body = html_template
            for k, v in r.get("variables", {}).items():
                body = body.replace(f"{{{{{k}}}}}", str(v))
            result = self.send(r["email"], subject, body)
            result["email"] = r["email"]
            results.append(result)
        return results

    def send_newsletter(self, recipient_list: list[str], subject: str, html: str) -> list[dict]:
        return self.send_bulk(
            [{"email": e, "name": "", "variables": {}} for e in recipient_list],
            subject,
            html,
        )
