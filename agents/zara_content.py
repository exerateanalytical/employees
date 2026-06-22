"""
ZARA — Content Creator
Writes blogs, product descriptions, case studies, video scripts, press releases.
"""

from __future__ import annotations

from .base_agent import BaseAgent


class ZaraContentAgent(BaseAgent):
    name = "ZARA"
    role = "Content Creator"
    emoji = "✍️"
    prompt_file = "zara_content.md"

    def write_blog(self, topic: str, keyword: str, icp: str, word_count: int = 1500) -> str:
        return self.run_task(
            f"Write a full SEO blog article:\n"
            f"Topic: {topic}\n"
            f"Primary keyword: {keyword}\n"
            f"Target reader: {icp}\n"
            f"Word count: {word_count}+\n\n"
            f"Follow the exact output format from your prompt. "
            f"Include meta description, slug, and internal link suggestions."
        )

    def write_product_description(self, product_id: str, extra_context: str = "") -> str:
        return self.run_task(
            f"Write a compelling product description for product ID: {product_id}\n"
            f"Extra context: {extra_context}\n\n"
            f"Use the $100M Offers value-first formula. "
            f"Include EN and FR versions. Follow your output format template."
        )

    def write_case_study(
        self,
        customer_type: str,
        country: str,
        problem: str,
        solution: str,
        result: str,
    ) -> str:
        return self.run_task(
            f"Write a compelling case study:\n"
            f"Customer type: {customer_type} ({country})\n"
            f"Problem they had: {problem}\n"
            f"How Opes helped: {solution}\n"
            f"Measurable result: {result}\n\n"
            f"Structure: Situation → Challenge → Solution → Results → Quote → Takeaway. "
            f"Make it vivid and specific. 600–1000 words."
        )

    def write_email_newsletter(self, theme: str, product_spotlight: str) -> str:
        return self.run_task(
            f"Write this week's email newsletter:\n"
            f"Theme: {theme}\n"
            f"Product spotlight: {product_spotlight}\n\n"
            f"Include: 5 subject line options, preview text, full body (EN + key section in FR). "
            f"Follow the newsletter structure from your prompt."
        )

    def write_video_script(self, product_or_topic: str, duration_seconds: int = 90) -> str:
        return self.run_task(
            f"Write a {duration_seconds}-second video script for: {product_or_topic}\n\n"
            f"Follow the timed script format from your prompt. "
            f"Include on-screen text suggestions and voiceover. EN version + FR voiceover."
        )

    def write_press_release(self, news: str, quote_source: str = "CEO") -> str:
        return self.run_task(
            f"Write a press release for: {news}\n"
            f"Executive quote from: {quote_source}\n\n"
            f"Follow the press release format from your prompt. "
            f"Make it newsworthy and distribution-ready."
        )

    def ghostwrite_linkedin(self, topic: str, voice: str = "founder") -> str:
        return self.run_task(
            f"Ghostwrite a LinkedIn article/post in the voice of the {voice}:\n"
            f"Topic: {topic}\n\n"
            f"The post should feel personal and insightful — written by a healthcare "
            f"entrepreneur who truly understands Africa. "
            f"1,000–1,500 words for article or 200–300 words for post. Specify which format."
        )

    def create_whatsapp_broadcast(self, message_theme: str) -> str:
        return self.run_task(
            f"Write a WhatsApp broadcast message for Opes customers:\n"
            f"Theme: {message_theme}\n\n"
            f"Keep it under 200 words, conversational, valuable, with one soft CTA. "
            f"English version + French version."
        )

    def record_top_content(self, content_type: str, topic: str, metrics: str) -> None:
        """Store a piece of content that performed well for future reference."""
        self.remember_success(
            approach=f"{content_type}: {topic}",
            result=metrics,
            context=f"Content type: {content_type}",
        )

    def learn_seo_insight(self, insight: str) -> None:
        """Store an SEO or content insight discovered from data or research."""
        self.learn(insight, source="ZARA content research")
