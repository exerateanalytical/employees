"""
AMARA — Social Media Manager
Generates platform-specific content, content calendars, and engagement strategies.
"""

from __future__ import annotations

from .base_agent import BaseAgent


class AmaraSocialAgent(BaseAgent):
    name = "AMARA"
    role = "Social Media Manager"
    emoji = "📱"
    prompt_file = "amara_social.md"

    # ── Public task methods ──────────────────────────────────────────────────

    def create_post(self, topic: str, platform: str, format: str = "image") -> str:
        return self.run_task(
            f"Create a {platform} {format} post about: {topic}\n"
            f"Include both English and French versions. "
            f"Follow the output format from your prompt exactly."
        )

    def create_weekly_calendar(self, theme: str | None = None) -> str:
        theme_note = f" Theme for this week: {theme}" if theme else ""
        return self.run_task(
            f"Create a complete 7-day social media content calendar for Opes Health Systems.{theme_note}\n"
            f"Cover all platforms: Facebook, Instagram, LinkedIn, Twitter/X, TikTok, WhatsApp.\n"
            f"Include EN + FR captions, posting times, hashtags, and goals for every post."
        )

    def respond_to_comment(self, comment: str, platform: str, context: str = "") -> str:
        return self.run_task(
            f"A user left this comment on our {platform} post:\n"
            f"'{comment}'\n"
            f"Context: {context}\n"
            f"Write a warm, on-brand reply in the same language as the comment. "
            f"If there is a sales opportunity, gently introduce it."
        )

    def analyse_content_performance(self, data: dict) -> str:
        import json
        return self.run_task(
            f"Analyse this week's social media performance and give strategic recommendations:\n"
            f"{json.dumps(data, indent=2)}\n"
            f"Tell me what's working, what isn't, and exactly what to change next week."
        )

    def create_campaign_content(self, product: str, campaign_goal: str) -> str:
        return self.run_task(
            f"Create a 5-post social media campaign for product: {product}\n"
            f"Campaign goal: {campaign_goal}\n"
            f"Include: teaser post, launch post, benefit post, testimonial post, CTA post.\n"
            f"All posts in EN + FR. Include hashtags, visuals direction, best posting times."
        )

    def record_top_post(self, platform: str, content_summary: str, metrics: str) -> None:
        """Call this when a post performs exceptionally well to teach AMARA what works."""
        self.remember_success(
            approach=f"{platform} post: {content_summary}",
            result=metrics,
            context=f"Platform: {platform}",
        )
