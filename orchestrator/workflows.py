"""
Pre-built multi-agent workflows for Opes Health Systems.

Each workflow wires specific agents in sequence, with each agent's output
feeding into the next agent's task. This creates compound intelligence:
the whole team produces what no single agent could.

Workflow catalogue:
  new_lead          — EMEKA researches → FATIMA writes onboarding → KOFI builds campaign
  tender_found      — ATLAS analyses → NOVA scores opportunity → ZARA writes proposal content → KOFI builds bid campaign
  content_campaign  — KOFI strategises → ZARA creates all content → AMARA schedules social
  competitor_alert  — ATLAS deep-dives → NOVA quantifies threat → KOFI builds counter-campaign
  customer_crisis   — CHISOM handles immediate → FATIMA plans recovery → NOVA tracks impact
  market_expansion  — ATLAS maps market → EMEKA finds first leads → KOFI builds entry campaign → NOVA forecasts
  weekly_review     — NOVA pulls metrics → all agents reflect → NOVA produces CEO report
  custom            — single free-text goal routed to the best single agent
"""

from __future__ import annotations

from typing import Any

from .pipeline import AgentPipeline


# ── Workflow definitions ─────────────────────────────────────────────────────

WORKFLOWS: dict[str, dict] = {
    "new_lead": {
        "description": "Full pipeline when a new qualified lead is identified",
        "params": {
            "lead_name": "Contact person name",
            "company": "Hospital / clinic / organisation name",
            "country": "Country",
            "product_interest": "Which OPES product they showed interest in",
            "context": "Any additional context about the lead",
        },
    },
    "tender_found": {
        "description": "Full pipeline when a tender or procurement opportunity is identified",
        "params": {
            "tender_title": "Title of the tender",
            "issuer": "Organisation issuing the tender",
            "country": "Country",
            "deadline": "Submission deadline",
            "description": "What the tender asks for",
        },
    },
    "content_campaign": {
        "description": "End-to-end content campaign: strategy → creation → social scheduling",
        "params": {
            "product": "OPES product to promote",
            "goal": "Campaign goal (leads, awareness, demo bookings, etc.)",
            "target_audience": "Who we are targeting",
            "duration": "Campaign duration (e.g. 30 days)",
        },
    },
    "competitor_alert": {
        "description": "Competitor intelligence → business impact → counter-campaign",
        "params": {
            "competitor": "Competitor name",
            "threat": "What they have done (new product, price drop, partnership, etc.)",
            "affected_products": "Which OPES products are most affected",
        },
    },
    "customer_crisis": {
        "description": "Customer issue → immediate response → recovery plan → impact tracking",
        "params": {
            "customer_name": "Customer contact name",
            "company": "Customer organisation",
            "product": "OPES product involved",
            "issue": "Description of the problem or complaint",
        },
    },
    "market_expansion": {
        "description": "Full market entry analysis → first leads → campaign → forecast",
        "params": {
            "country": "Target country to expand into",
            "product_focus": "Primary OPES product for entry",
        },
    },
    "weekly_review": {
        "description": "Full weekly intelligence and performance review across all agents",
        "params": {
            "week": "Week identifier (e.g. Week 24, June 2026)",
            "highlights": "Any specific events or milestones this week",
        },
    },
    "custom": {
        "description": "Free-form goal routed to the most appropriate agent",
        "params": {
            "goal": "Full description of what you want to achieve",
        },
    },
}


# ── Workflow builders ────────────────────────────────────────────────────────

def _new_lead(params: dict) -> AgentPipeline:
    p = AgentPipeline("new_lead")
    lead = params.get("lead_name", "the contact")
    company = params.get("company", "the organisation")
    country = params.get("country", "Africa")
    product = params.get("product_interest", "OPES Health Systems products")
    context = params.get("context", "")

    p.add_step(
        "emeka",
        task_fn=lambda ctx: (
            f"Research this new lead and produce a full qualification brief:\n"
            f"Contact: {lead} at {company} ({country})\n"
            f"Product interest: {product}\n"
            f"Context: {context}\n\n"
            f"Produce: Organisation profile, decision-maker analysis, budget signals, "
            f"BANT qualification, lead tier (A/B/C), recommended first approach, "
            f"and 5 personalised talking points for this specific organisation."
        ),
        label="Lead research & qualification",
        store_as="lead_research",
    )

    p.add_step(
        "fatima",
        task_fn=lambda ctx: (
            f"A new lead has been qualified. Create their personalised outreach sequence.\n\n"
            f"LEAD INTELLIGENCE FROM EMEKA:\n{ctx.get('lead_research', '')}\n\n"
            f"Create:\n"
            f"1. An immediate WhatsApp/email introduction message (Day 0)\n"
            f"2. A 14-day nurture sequence (Day 3, 7, 14) — each with EN + FR versions\n"
            f"3. A demo booking ask for Day 7\n"
            f"4. A 'gone quiet' re-engagement message for Day 30\n"
            f"Each message must reference specific details about {company} from the research above."
        ),
        label="Personalised outreach sequence",
        store_as="outreach_sequence",
    )

    p.add_step(
        "kofi",
        task_fn=lambda ctx: (
            f"Build a mini-campaign to convert this qualified lead into a demo booking.\n\n"
            f"LEAD: {lead} at {company} ({country})\n"
            f"PRODUCT INTEREST: {product}\n\n"
            f"EMEKA'S RESEARCH:\n{ctx.get('lead_research', '')[:600]}\n\n"
            f"Create:\n"
            f"1. A Grand Slam Offer specifically designed for this lead's pain points\n"
            f"2. One LinkedIn message to connect with {lead}\n"
            f"3. One personalised email campaign (3 emails) using Hormozi's sequence framework\n"
            f"4. A demo call agenda tailored to {company}'s specific situation"
        ),
        label="Conversion campaign",
        store_as="conversion_campaign",
    )

    p.add_step(
        "nova",
        task_fn=lambda ctx: (
            f"Score this lead opportunity and produce an executive brief for the CEO.\n\n"
            f"LEAD: {lead} at {company} ({country}) | Product: {product}\n\n"
            f"EMEKA RESEARCH: {ctx.get('lead_research', '')[:400]}\n"
            f"OUTREACH PLAN: {ctx.get('outreach_sequence', '')[:300]}\n"
            f"CAMPAIGN: {ctx.get('conversion_campaign', '')[:300]}\n\n"
            f"Produce:\n"
            f"- Estimated deal value in FCFA\n"
            f"- Win probability (%)\n"
            f"- Expected close timeline\n"
            f"- Top 3 risks\n"
            f"- CEO action required (if any)\n"
            f"- This lead's rank in our current pipeline"
        ),
        label="Opportunity scoring & CEO brief",
        store_as="opportunity_brief",
    )

    return p


def _tender_found(params: dict) -> AgentPipeline:
    p = AgentPipeline("tender_found")
    title = params.get("tender_title", "the tender")
    issuer = params.get("issuer", "the issuing body")
    country = params.get("country", "")
    deadline = params.get("deadline", "TBD")
    description = params.get("description", "")

    p.add_step(
        "atlas",
        task_fn=lambda ctx: (
            f"Analyse this tender opportunity in detail:\n"
            f"Title: {title}\n"
            f"Issuer: {issuer} ({country})\n"
            f"Deadline: {deadline}\n"
            f"Description: {description}\n\n"
            f"Produce:\n"
            f"1. Which OPES products are the best fit and why\n"
            f"2. Likely evaluation criteria and scoring weights\n"
            f"3. Main competitors who will probably bid\n"
            f"4. Our competitive advantages in this specific tender\n"
            f"5. Intelligence gaps we need to fill before submitting\n"
            f"6. GO / NO-GO recommendation with reasoning"
        ),
        label="Tender intelligence analysis",
        store_as="tender_analysis",
    )

    p.add_step(
        "nova",
        task_fn=lambda ctx: (
            f"Score this tender as a business opportunity.\n\n"
            f"TENDER: {title} | Issuer: {issuer} | Deadline: {deadline}\n\n"
            f"ATLAS ANALYSIS:\n{ctx.get('tender_analysis', '')[:600]}\n\n"
            f"Produce:\n"
            f"- Estimated contract value (FCFA range)\n"
            f"- Win probability given our competitive position\n"
            f"- Resource investment required to bid (person-days, costs)\n"
            f"- ROI on bidding effort\n"
            f"- Priority ranking vs. other active opportunities\n"
            f"- Final GO / NO-GO decision with financial justification"
        ),
        label="Financial opportunity scoring",
        store_as="tender_score",
    )

    p.add_step(
        "zara",
        task_fn=lambda ctx: (
            f"Write the core content needed for this tender bid.\n\n"
            f"TENDER: {title} | Issuer: {issuer} ({country})\n\n"
            f"ANALYSIS: {ctx.get('tender_analysis', '')[:500]}\n\n"
            f"Produce (all in English AND French):\n"
            f"1. Executive summary (250 words) — why OPES is the right choice\n"
            f"2. Company profile section tailored to this tender\n"
            f"3. Product/solution description matching the tender requirements\n"
            f"4. Three case study paragraphs showing relevant experience\n"
            f"5. Value proposition statement specific to {issuer}"
        ),
        label="Tender bid content writing",
        store_as="tender_content",
    )

    p.add_step(
        "kofi",
        task_fn=lambda ctx: (
            f"Build a relationship campaign to support our bid for this tender.\n\n"
            f"TENDER: {title} | Issuer: {issuer} ({country}) | Deadline: {deadline}\n\n"
            f"While we prepare our technical bid, we need to build relationships with "
            f"decision-makers at {issuer}. Create:\n"
            f"1. A stakeholder mapping plan (who to approach, in what order)\n"
            f"2. LinkedIn outreach messages for the top 3 decision-maker titles\n"
            f"3. A thought leadership content piece to share with {issuer} contacts\n"
            f"4. An email to request a pre-submission clarification meeting"
        ),
        label="Relationship-building campaign",
        store_as="bid_campaign",
    )

    return p


def _content_campaign(params: dict) -> AgentPipeline:
    p = AgentPipeline("content_campaign")
    product = params.get("product", "OPES Health Systems")
    goal = params.get("goal", "generate leads")
    audience = params.get("target_audience", "hospital directors in CEMAC")
    duration = params.get("duration", "30 days")

    p.add_step(
        "kofi",
        task_fn=lambda ctx: (
            f"Build the complete content marketing strategy:\n"
            f"Product: {product}\n"
            f"Goal: {goal}\n"
            f"Target audience: {audience}\n"
            f"Duration: {duration}\n\n"
            f"Apply the Grand Slam Offer + Core 4 traffic framework. Produce:\n"
            f"1. Campaign theme and positioning\n"
            f"2. Core value proposition and messaging pillars\n"
            f"3. Content mix by channel (LinkedIn, Facebook, Email, WhatsApp)\n"
            f"4. Content calendar overview (week by week)\n"
            f"5. Lead magnet concept\n"
            f"6. KPIs and measurement framework"
        ),
        label="Campaign strategy",
        store_as="campaign_strategy",
    )

    p.add_step(
        "zara",
        task_fn=lambda ctx: (
            f"Create all content assets for this campaign.\n\n"
            f"STRATEGY FROM KOFI:\n{ctx.get('campaign_strategy', '')[:800]}\n\n"
            f"Produce the following (all EN + FR):\n"
            f"1. Long-form blog post (1,000 words) — the anchor content\n"
            f"2. Email newsletter (with 5 subject line options)\n"
            f"3. WhatsApp broadcast message\n"
            f"4. LinkedIn article (600 words)\n"
            f"5. Lead magnet outline (the promised resource)\n"
            f"All content must align with the strategy messaging above."
        ),
        label="Content creation (all formats)",
        store_as="content_assets",
    )

    p.add_step(
        "amara",
        task_fn=lambda ctx: (
            f"Create the social media execution plan for this campaign.\n\n"
            f"STRATEGY:\n{ctx.get('campaign_strategy', '')[:400]}\n\n"
            f"CONTENT ASSETS AVAILABLE:\n{ctx.get('content_assets', '')[:400]}\n\n"
            f"Produce:\n"
            f"1. A 4-week social media content calendar (all platforms)\n"
            f"2. 8 platform-specific posts (Facebook, Instagram, LinkedIn, Twitter/X) — EN + FR each\n"
            f"3. 2 TikTok/Reels scripts (60 seconds each)\n"
            f"4. Posting schedule with optimal times for CEMAC audience\n"
            f"5. Hashtag strategy by platform"
        ),
        label="Social media execution",
        store_as="social_plan",
    )

    return p


def _competitor_alert(params: dict) -> AgentPipeline:
    p = AgentPipeline("competitor_alert")
    competitor = params.get("competitor", "a competitor")
    threat = params.get("threat", "a competitive move")
    products = params.get("affected_products", "our core products")

    p.add_step(
        "atlas",
        task_fn=lambda ctx: (
            f"URGENT: Competitive threat analysis needed.\n\n"
            f"Competitor: {competitor}\n"
            f"What they have done: {threat}\n"
            f"OPES products most affected: {products}\n\n"
            f"Produce:\n"
            f"1. Full analysis of what {competitor} has done and why\n"
            f"2. How this changes the competitive landscape in CEMAC\n"
            f"3. Which of our customers/prospects are most at risk of switching\n"
            f"4. Their likely next moves\n"
            f"5. Our 3 strongest competitive advantages vs. this specific threat\n"
            f"6. Immediate actions OPES should take in the next 7 days"
        ),
        label="Competitive threat intelligence",
        store_as="threat_analysis",
    )

    p.add_step(
        "nova",
        task_fn=lambda ctx: (
            f"Quantify the business impact of this competitive threat.\n\n"
            f"Competitor: {competitor} | Threat: {threat}\n\n"
            f"ATLAS ANALYSIS:\n{ctx.get('threat_analysis', '')[:600]}\n\n"
            f"Produce:\n"
            f"- Estimated revenue at risk (FCFA)\n"
            f"- Number of accounts/prospects at risk\n"
            f"- Probability of losing accounts without action vs. with action\n"
            f"- Budget recommended for counter-campaign\n"
            f"- CEO briefing (5 bullet points, board-ready)"
        ),
        label="Business impact quantification",
        store_as="impact_assessment",
    )

    p.add_step(
        "kofi",
        task_fn=lambda ctx: (
            f"Build an urgent counter-campaign against {competitor}.\n\n"
            f"THREAT: {threat}\n"
            f"AFFECTED PRODUCTS: {products}\n\n"
            f"INTELLIGENCE: {ctx.get('threat_analysis', '')[:400]}\n"
            f"IMPACT: {ctx.get('impact_assessment', '')[:300]}\n\n"
            f"Create (launch-ready in 48 hours):\n"
            f"1. Counter-positioning statement (what we say now to prospects)\n"
            f"2. Competitive battle card (our rep uses this in every sales call)\n"
            f"3. Emergency email to at-risk existing customers (EN + FR)\n"
            f"4. LinkedIn campaign targeting prospects {competitor} is approaching\n"
            f"5. Updated objection handling for '{competitor} is cheaper/better'"
        ),
        label="Counter-campaign (48-hour launch)",
        store_as="counter_campaign",
    )

    p.add_step(
        "chisom",
        task_fn=lambda ctx: (
            f"Prepare the customer service team to handle {competitor}-related inquiries.\n\n"
            f"THREAT: {threat}\n\n"
            f"Customers may ask us directly about {competitor}. Prepare:\n"
            f"1. Script for 'I heard {competitor} just launched X — what does OPES offer?'\n"
            f"2. Script for 'Is OPES cheaper than {competitor}?'\n"
            f"3. Script for 'A friend recommended {competitor} instead of OPES'\n"
            f"4. Escalation protocol if a customer says they are switching to {competitor}\n"
            f"All in EN + FR."
        ),
        label="Customer service battle scripts",
        store_as="battle_scripts",
    )

    return p


def _customer_crisis(params: dict) -> AgentPipeline:
    p = AgentPipeline("customer_crisis")
    customer = params.get("customer_name", "the customer")
    company = params.get("company", "their organisation")
    product = params.get("product", "OPES product")
    issue = params.get("issue", "a critical issue")

    p.add_step(
        "chisom",
        task_fn=lambda ctx: (
            f"URGENT: Customer crisis response needed.\n\n"
            f"Customer: {customer} at {company}\n"
            f"Product: {product}\n"
            f"Issue: {issue}\n\n"
            f"Produce immediately:\n"
            f"1. Acknowledgement message to send within 5 minutes (WhatsApp + email, EN + FR)\n"
            f"2. Internal escalation brief for the technical team\n"
            f"3. Customer-facing timeline commitment message\n"
            f"4. Status update templates (for hourly updates if needed)\n"
            f"5. Resolution confirmation message\n"
            f"Use the RECEIVE→ACKNOWLEDGE→INVESTIGATE→RESOLVE→FOLLOW UP protocol."
        ),
        label="Immediate crisis response",
        store_as="crisis_response",
    )

    p.add_step(
        "fatima",
        task_fn=lambda ctx: (
            f"Design a recovery plan to rebuild trust with {customer} at {company}.\n\n"
            f"ISSUE: {issue}\n"
            f"IMMEDIATE RESPONSE ALREADY SENT:\n{ctx.get('crisis_response', '')[:400]}\n\n"
            f"Create a 30-day trust recovery plan:\n"
            f"1. Goodwill gesture (what to offer — discount on next order? free training? extended support?)\n"
            f"2. Day 3 follow-up (is the resolution holding?)\n"
            f"3. Day 7 check-in with account review offer\n"
            f"4. Day 14 proactive value delivery (training session, product tip, etc.)\n"
            f"5. Day 30 satisfaction check and referral/testimonial ask\n"
            f"All messages EN + FR. Make them feel genuinely cared for."
        ),
        label="Trust recovery plan",
        store_as="recovery_plan",
    )

    p.add_step(
        "nova",
        task_fn=lambda ctx: (
            f"Assess the business impact of this customer crisis and what we can learn.\n\n"
            f"CUSTOMER: {customer} at {company} | PRODUCT: {product}\n"
            f"ISSUE: {issue}\n\n"
            f"Produce:\n"
            f"1. Revenue at risk if we lose this customer\n"
            f"2. Referral value at risk (how many other prospects could they influence?)\n"
            f"3. Root cause category (product bug / implementation / training / expectation?)\n"
            f"4. Is this a systemic issue? Could other customers face the same?\n"
            f"5. Process improvement recommendation to prevent recurrence\n"
            f"6. 3-line CEO summary"
        ),
        label="Impact analysis & lessons learned",
        store_as="crisis_analysis",
    )

    return p


def _market_expansion(params: dict) -> AgentPipeline:
    p = AgentPipeline("market_expansion")
    country = params.get("country", "a new African market")
    product = params.get("product_focus", "OPES EMR")

    p.add_step(
        "atlas",
        task_fn=lambda ctx: (
            f"Produce a comprehensive market entry intelligence report for: {country}\n\n"
            f"Primary product for entry: {product}\n\n"
            f"Cover in full:\n"
            f"1. Healthcare system overview (public/private split, funding, bed count)\n"
            f"2. Digital health readiness (internet penetration, smartphone adoption, existing HIS)\n"
            f"3. Regulatory environment (Ministry of Health, data protection laws, procurement rules)\n"
            f"4. Key institutions and decision-makers to target\n"
            f"5. Active competitors already operating in this market\n"
            f"6. Cultural and language considerations for OPES\n"
            f"7. Active tenders/procurement opportunities\n"
            f"8. GO / WAIT / NO-GO recommendation with reasoning"
        ),
        label="Market intelligence report",
        store_as="market_intel",
    )

    p.add_step(
        "emeka",
        task_fn=lambda ctx: (
            f"Identify the first 20 leads for OPES entering {country}.\n\n"
            f"Product: {product}\n\n"
            f"MARKET INTELLIGENCE:\n{ctx.get('market_intel', '')[:600]}\n\n"
            f"Produce:\n"
            f"1. 20 target organisations with: name, type, size, city, why they need {product}\n"
            f"2. Top 5 Tier-A leads with full contact strategy\n"
            f"3. The 3 best entry channels for this market (LinkedIn, WhatsApp, events, MOH, etc.)\n"
            f"4. A cold outreach sequence localised for {country} (EN + local language if applicable)"
        ),
        label="First-wave lead identification",
        store_as="market_leads",
    )

    p.add_step(
        "kofi",
        task_fn=lambda ctx: (
            f"Build the market entry campaign for OPES in {country}.\n\n"
            f"PRODUCT: {product}\n\n"
            f"MARKET INTEL: {ctx.get('market_intel', '')[:400]}\n"
            f"LEADS: {ctx.get('market_leads', '')[:400]}\n\n"
            f"Create the full 90-day market entry campaign:\n"
            f"1. Entry positioning (how OPES is different from anything they've seen before)\n"
            f"2. Month 1: Awareness phase — channels, content, ad copy\n"
            f"3. Month 2: Lead nurture — email sequence, WhatsApp campaign\n"
            f"4. Month 3: Conversion phase — demo offer, partnership approach\n"
            f"5. Local partnership strategy (WHO offices, health NGOs, distributors)\n"
            f"6. Budget allocation by channel"
        ),
        label="90-day market entry campaign",
        store_as="entry_campaign",
    )

    p.add_step(
        "nova",
        task_fn=lambda ctx: (
            f"Produce the financial business case for entering {country}.\n\n"
            f"PRODUCT: {product}\n\n"
            f"MARKET: {ctx.get('market_intel', '')[:300]}\n"
            f"CAMPAIGN COST ESTIMATE: {ctx.get('entry_campaign', '')[:200]}\n\n"
            f"Produce:\n"
            f"1. Total addressable market (TAM) in FCFA\n"
            f"2. Year 1 revenue target (realistic)\n"
            f"3. Break-even timeline\n"
            f"4. Investment required (marketing + operations + legal)\n"
            f"5. 3-scenario forecast (base / optimistic / pessimistic)\n"
            f"6. Board-ready recommendation: Enter now / Enter in 6 months / Don't enter"
        ),
        label="Financial business case",
        store_as="financial_case",
    )

    return p


def _weekly_review(params: dict) -> AgentPipeline:
    p = AgentPipeline("weekly_review")
    week = params.get("week", "this week")
    highlights = params.get("highlights", "")

    p.add_step(
        "atlas",
        task_fn=lambda ctx: (
            f"Produce the weekly competitive and market intelligence summary for {week}.\n"
            f"Highlights to incorporate: {highlights}\n\n"
            f"Cover: competitor moves, market news, tender alerts, "
            f"country spotlight (pick one CEMAC country), and top 3 opportunities spotted."
        ),
        label="Market & competitive intel",
        store_as="market_intel",
    )

    p.add_step(
        "emeka",
        task_fn=lambda ctx: (
            f"Produce the weekly lead generation performance report for {week}.\n\n"
            f"Include: leads researched, outreach sequences active, response rates observed, "
            f"hottest leads ready for handoff to FATIMA, and next week's prospecting priorities."
        ),
        label="Lead generation report",
        store_as="leads_report",
    )

    p.add_step(
        "amara",
        task_fn=lambda ctx: (
            f"Produce the weekly social media performance report for {week}.\n\n"
            f"Assess: what content worked best, platform-by-platform summary, "
            f"top-performing post format, what to replicate next week, "
            f"and the social media plan for next week."
        ),
        label="Social media performance",
        store_as="social_report",
    )

    p.add_step(
        "nova",
        task_fn=lambda ctx: (
            f"Produce the weekly CEO dashboard for {week}.\n\n"
            f"MARKET INTEL:\n{ctx.get('market_intel', '')[:400]}\n\n"
            f"LEADS REPORT:\n{ctx.get('leads_report', '')[:400]}\n\n"
            f"SOCIAL MEDIA:\n{ctx.get('social_report', '')[:400]}\n\n"
            f"Compile into the CEO Dashboard format:\n"
            f"TL;DR (3 bullets) → Revenue Snapshot → Pipeline → AI Team Performance → "
            f"Alerts / Watches / Wins → 3 Concrete CEO Actions for next week."
        ),
        label="CEO dashboard compilation",
        store_as="ceo_dashboard",
    )

    return p


def _custom(params: dict) -> AgentPipeline:
    """Route a free-form goal to the single most appropriate agent."""
    p = AgentPipeline("custom")
    goal = params.get("goal", "Help with an OPES task")

    # Use NOVA as the default router for custom goals
    p.add_step(
        "nova",
        task_fn=lambda ctx: (
            f"The following task has been submitted to the OPES AI team:\n\n{goal}\n\n"
            f"Analyse this request and produce the best possible output, drawing on all "
            f"your business intelligence capabilities. If this would be better handled by "
            f"a different team member, say so explicitly at the start of your response."
        ),
        label="Custom goal execution",
        store_as="custom_output",
    )
    return p


# ── Registry ─────────────────────────────────────────────────────────────────

_BUILDERS = {
    "new_lead": _new_lead,
    "tender_found": _tender_found,
    "content_campaign": _content_campaign,
    "competitor_alert": _competitor_alert,
    "customer_crisis": _customer_crisis,
    "market_expansion": _market_expansion,
    "weekly_review": _weekly_review,
    "custom": _custom,
}


def build_workflow(workflow_id: str, params: dict) -> AgentPipeline:
    builder = _BUILDERS.get(workflow_id, _custom)
    return builder(params)
