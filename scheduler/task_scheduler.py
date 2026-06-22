"""
APScheduler task definitions — what each AI employee does automatically and when.
Times are in Africa/Douala timezone (UTC+1, covers CEMAC + West Africa).
"""

from __future__ import annotations

import logging

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from agents import (
    AmaraSocialAgent,
    AtlasResearchAgent,
    ChisomServiceAgent,
    EmekaLeadsAgent,
    FatimaOutreachAgent,
    KofiMarketingAgent,
    NovaAnalyticsAgent,
    ZaraContentAgent,
)

log = logging.getLogger(__name__)
TZ = "Africa/Douala"


# ── Scheduled task functions ─────────────────────────────────────────────────

def amara_morning_posts():
    """AMARA creates the morning social posts (7am)."""
    agent = AmaraSocialAgent()
    agent.create_post(
        topic="Start your Monday with a health tip for African healthcare teams",
        platform="Facebook",
        format="image",
    )
    log.info("AMARA: morning posts created")


def amara_evening_engagement():
    """AMARA creates evening engagement content (6pm)."""
    agent = AmaraSocialAgent()
    agent.run_task(
        "Create an engaging evening post for all platforms. "
        "Use a question or poll format to drive comments. "
        "Topic: [Choose the most relevant current health topic for Africa]"
    )
    log.info("AMARA: evening engagement posts created")


def chisom_faq_review():
    """CHISOM reviews and updates FAQs weekly (Monday 9am)."""
    agent = ChisomServiceAgent()
    agent.run_task(
        "Review our current FAQs and identify: "
        "1. Questions we're missing based on common customer queries "
        "2. Answers that need updating "
        "3. New FAQs to add for products launched in the last month "
        "Produce an updated FAQ document."
    )
    log.info("CHISOM: FAQ review completed")


def kofi_weekly_email():
    """KOFI drafts the weekly email newsletter brief (Tuesday 9am)."""
    agent = KofiMarketingAgent()
    agent.run_task(
        "Plan this week's email newsletter campaign. "
        "Pick the most relevant topic for our current business priorities. "
        "Produce a campaign brief with: subject lines, key messages, product spotlight, CTA. "
        "Hand off to ZARA for full copy."
    )
    log.info("KOFI: weekly email brief created")


def zara_blog_draft():
    """ZARA drafts one SEO blog article per week (Wednesday 10am)."""
    agent = ZaraContentAgent()
    agent.run_task(
        "Write this week's SEO blog article. "
        "Choose the highest-value keyword opportunity for our African healthcare audience. "
        "Full 1,500-word article with meta description, slug, and internal link suggestions."
    )
    log.info("ZARA: weekly blog draft created")


def emeka_prospect_research():
    """EMEKA researches new prospects (Monday, Wednesday, Friday 8am)."""
    agent = EmekaLeadsAgent()
    agent.run_task(
        "Research 20 new qualified prospects for Opes Health Systems today. "
        "Mix: 10 hospitals/clinics, 5 pharmacies/distributors, 5 NGOs or government contacts. "
        "Spread across at least 3 different African countries. "
        "Format using the Lead Tracking Template. Tier each lead A/B/C."
    )
    log.info("EMEKA: prospect research completed")


def emeka_outreach_review():
    """EMEKA reviews and optimizes outreach sequences (Thursday 9am)."""
    agent = EmekaLeadsAgent()
    agent.run_task(
        "Review our current outreach sequences. "
        "Identify: which sequences have the best response rates, "
        "what to improve in underperforming sequences, "
        "any new segments that need bespoke outreach sequences. "
        "Produce optimized versions of the 2 lowest-performing sequences."
    )
    log.info("EMEKA: outreach review completed")


def fatima_reengagement_check():
    """FATIMA identifies customers needing re-engagement (Tuesday 9am)."""
    from tools.crm_tools import CRMTools
    crm = CRMTools()
    at_risk = crm.get_at_risk_customers(inactive_days=90)

    if not at_risk:
        log.info("FATIMA: no at-risk customers today")
        return

    agent = FatimaOutreachAgent()
    customer_list = "\n".join(
        f"- {c.contact_name} at {c.company} ({c.country}), "
        f"last order: {c.last_order_date.strftime('%Y-%m-%d') if c.last_order_date else 'unknown'}"
        for c in at_risk[:20]
    )
    agent.run_task(
        f"These customers haven't ordered in 90+ days. Create re-engagement messages:\n"
        f"{customer_list}\n\n"
        f"Write personalised WhatsApp messages for each. Group similar customers and "
        f"write one batch message per group."
    )
    log.info(f"FATIMA: re-engagement messages created for {len(at_risk)} customers")


def atlas_weekly_intel():
    """ATLAS produces the weekly intelligence report (Friday 8am)."""
    agent = AtlasResearchAgent()
    agent.produce_weekly_intel_report()
    log.info("ATLAS: weekly intelligence report produced")


def atlas_tender_scan():
    """ATLAS scans for new tenders (Monday, Wednesday 7am)."""
    agent = AtlasResearchAgent()
    agent.find_tenders(
        product_category="[Fill with your main product categories]",
        region="Africa"
    )
    log.info("ATLAS: tender scan completed")


def evolve_all_agents():
    """Phase 3: Run one evolution cycle for all 8 agents (Sunday 2am)."""
    from improver import ABTester
    from improver.benchmarks import BENCHMARK_TASKS
    tester = ABTester()
    results = tester.run_full_team(BENCHMARK_TASKS, verbose=False)
    improved = sum(1 for r in results if r["winner"] == "mutant")
    log.info(f"EVOLUTION: {improved}/{len(results)} agents improved this cycle")


def nova_weekly_report():
    """NOVA produces the weekly CEO dashboard (Monday 7am)."""
    from tools.crm_tools import CRMTools
    crm = CRMTools()
    pipeline = crm.pipeline_summary()
    revenue = crm.revenue_by_country()

    agent = NovaAnalyticsAgent()
    agent.weekly_ceo_report({
        "pipeline": pipeline,
        "revenue_by_country": revenue,
        "note": "Populate with actual sales data from your CRM/ERP",
    })
    log.info("NOVA: weekly CEO report produced")


# ── Scheduler setup ───────────────────────────────────────────────────────────

def build_scheduler() -> BackgroundScheduler:
    scheduler = BackgroundScheduler(timezone=TZ)

    # AMARA — Daily social content
    scheduler.add_job(amara_morning_posts, CronTrigger(hour=7, minute=0, timezone=TZ), id="amara_morning")
    scheduler.add_job(amara_evening_engagement, CronTrigger(hour=18, minute=0, timezone=TZ), id="amara_evening")

    # CHISOM — Weekly FAQ review
    scheduler.add_job(chisom_faq_review, CronTrigger(day_of_week="mon", hour=9, timezone=TZ), id="chisom_faq")

    # KOFI — Weekly email brief
    scheduler.add_job(kofi_weekly_email, CronTrigger(day_of_week="tue", hour=9, timezone=TZ), id="kofi_email")

    # ZARA — Weekly blog
    scheduler.add_job(zara_blog_draft, CronTrigger(day_of_week="wed", hour=10, timezone=TZ), id="zara_blog")

    # EMEKA — Lead research 3x/week, outreach review 1x/week
    scheduler.add_job(emeka_prospect_research, CronTrigger(day_of_week="mon,wed,fri", hour=8, timezone=TZ), id="emeka_prospects")
    scheduler.add_job(emeka_outreach_review, CronTrigger(day_of_week="thu", hour=9, timezone=TZ), id="emeka_review")

    # FATIMA — Weekly re-engagement
    scheduler.add_job(fatima_reengagement_check, CronTrigger(day_of_week="tue", hour=9, timezone=TZ), id="fatima_reengagement")

    # ATLAS — Weekly intel + 2x tender scans
    scheduler.add_job(atlas_weekly_intel, CronTrigger(day_of_week="fri", hour=8, timezone=TZ), id="atlas_intel")
    scheduler.add_job(atlas_tender_scan, CronTrigger(day_of_week="mon,wed", hour=7, timezone=TZ), id="atlas_tenders")

    # NOVA — Weekly CEO report (Monday before the team starts work)
    scheduler.add_job(nova_weekly_report, CronTrigger(day_of_week="mon", hour=7, timezone=TZ), id="nova_weekly")

    # PHASE 3 — Automatic prompt evolution every Sunday at 2am
    scheduler.add_job(evolve_all_agents, CronTrigger(day_of_week="sun", hour=2, timezone=TZ), id="evolution")

    return scheduler
