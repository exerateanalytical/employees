"""
FastAPI — REST API for all 8 Opes AI employees.
Deploy this to receive requests from your website, CRM, or front-end dashboard.
"""

from __future__ import annotations

import os
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

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
from scheduler import build_scheduler

security = HTTPBearer()
scheduler = build_scheduler()


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.start()
    yield
    scheduler.shutdown()


app = FastAPI(
    title="Opes Health Systems — AI Employees API",
    description="8 AI employees serving healthcare across Africa",
    version="1.0.0",
    lifespan=lifespan,
)


def _verify_token(credentials: HTTPAuthorizationCredentials = Security(security)) -> str:
    expected = os.environ.get("SECRET_KEY", "")
    if credentials.credentials != expected:
        raise HTTPException(status_code=401, detail="Invalid token")
    return credentials.credentials


# ── Request / Response Models ────────────────────────────────────────────────

class TaskRequest(BaseModel):
    task: str
    context: dict[str, Any] = {}


class AgentResponse(BaseModel):
    agent: str
    result: str


# ── AMARA Endpoints ──────────────────────────────────────────────────────────

class SocialPostRequest(BaseModel):
    topic: str
    platform: str
    format: str = "image"


class ContentCalendarRequest(BaseModel):
    theme: str | None = None


@app.post("/amara/post", response_model=AgentResponse, tags=["AMARA"])
async def create_social_post(req: SocialPostRequest, token: str = Security(_verify_token)):
    agent = AmaraSocialAgent()
    return AgentResponse(agent="AMARA", result=agent.create_post(req.topic, req.platform, req.format))


@app.post("/amara/calendar", response_model=AgentResponse, tags=["AMARA"])
async def create_content_calendar(req: ContentCalendarRequest, token: str = Security(_verify_token)):
    agent = AmaraSocialAgent()
    return AgentResponse(agent="AMARA", result=agent.create_weekly_calendar(req.theme))


# ── CHISOM Endpoints ─────────────────────────────────────────────────────────

class InquiryRequest(BaseModel):
    message: str
    customer_name: str = ""
    channel: str = "email"


@app.post("/chisom/inquiry", response_model=AgentResponse, tags=["CHISOM"])
async def handle_customer_inquiry(req: InquiryRequest, token: str = Security(_verify_token)):
    agent = ChisomServiceAgent()
    return AgentResponse(
        agent="CHISOM",
        result=agent.handle_inquiry(req.message, req.customer_name, req.channel)
    )


class ComplaintRequest(BaseModel):
    complaint: str
    customer_name: str
    product: str = ""


@app.post("/chisom/complaint", response_model=AgentResponse, tags=["CHISOM"])
async def handle_complaint(req: ComplaintRequest, token: str = Security(_verify_token)):
    agent = ChisomServiceAgent()
    return AgentResponse(
        agent="CHISOM",
        result=agent.handle_complaint(req.complaint, req.customer_name, req.product)
    )


# ── KOFI Endpoints ───────────────────────────────────────────────────────────

class CampaignRequest(BaseModel):
    product: str
    goal: str
    budget: str
    duration: str


@app.post("/kofi/campaign", response_model=AgentResponse, tags=["KOFI"])
async def build_campaign(req: CampaignRequest, token: str = Security(_verify_token)):
    agent = KofiMarketingAgent()
    return AgentResponse(
        agent="KOFI",
        result=agent.build_campaign(req.product, req.goal, req.budget, req.duration)
    )


class EmailSequenceRequest(BaseModel):
    icp: str
    product: str
    sequence_type: str = "welcome"


@app.post("/kofi/email-sequence", response_model=AgentResponse, tags=["KOFI"])
async def write_email_sequence(req: EmailSequenceRequest, token: str = Security(_verify_token)):
    agent = KofiMarketingAgent()
    return AgentResponse(
        agent="KOFI",
        result=agent.write_email_sequence(req.icp, req.product, req.sequence_type)
    )


# ── ZARA Endpoints ───────────────────────────────────────────────────────────

class BlogRequest(BaseModel):
    topic: str
    keyword: str
    icp: str
    word_count: int = 1500


@app.post("/zara/blog", response_model=AgentResponse, tags=["ZARA"])
async def write_blog(req: BlogRequest, token: str = Security(_verify_token)):
    agent = ZaraContentAgent()
    return AgentResponse(
        agent="ZARA",
        result=agent.write_blog(req.topic, req.keyword, req.icp, req.word_count)
    )


class ProductDescRequest(BaseModel):
    product_id: str
    extra_context: str = ""


@app.post("/zara/product-description", response_model=AgentResponse, tags=["ZARA"])
async def write_product_description(req: ProductDescRequest, token: str = Security(_verify_token)):
    agent = ZaraContentAgent()
    return AgentResponse(
        agent="ZARA",
        result=agent.write_product_description(req.product_id, req.extra_context)
    )


# ── EMEKA Endpoints ──────────────────────────────────────────────────────────

class ProspectResearchRequest(BaseModel):
    segment: str
    country: str
    count: int = 20


@app.post("/emeka/prospects", response_model=AgentResponse, tags=["EMEKA"])
async def research_prospects(req: ProspectResearchRequest, token: str = Security(_verify_token)):
    agent = EmekaLeadsAgent()
    return AgentResponse(
        agent="EMEKA",
        result=agent.research_prospects(req.segment, req.country, req.count)
    )


class OutreachSequenceRequest(BaseModel):
    segment: str
    country: str
    product: str


@app.post("/emeka/outreach-sequence", response_model=AgentResponse, tags=["EMEKA"])
async def write_outreach_sequence(req: OutreachSequenceRequest, token: str = Security(_verify_token)):
    agent = EmekaLeadsAgent()
    return AgentResponse(
        agent="EMEKA",
        result=agent.write_outreach_sequence(req.segment, req.country, req.product)
    )


# ── FATIMA Endpoints ─────────────────────────────────────────────────────────

class OnboardingRequest(BaseModel):
    customer_name: str
    company: str
    product: str
    country: str


@app.post("/fatima/onboard", response_model=AgentResponse, tags=["FATIMA"])
async def onboard_customer(req: OnboardingRequest, token: str = Security(_verify_token)):
    agent = FatimaOutreachAgent()
    return AgentResponse(
        agent="FATIMA",
        result=agent.onboard_customer(req.customer_name, req.company, req.product, req.country)
    )


# ── ATLAS Endpoints ──────────────────────────────────────────────────────────

class CompetitorRequest(BaseModel):
    competitor_name: str
    website: str
    context: str = ""


@app.post("/atlas/competitor", response_model=AgentResponse, tags=["ATLAS"])
async def analyze_competitor(req: CompetitorRequest, token: str = Security(_verify_token)):
    agent = AtlasResearchAgent()
    return AgentResponse(
        agent="ATLAS",
        result=agent.analyze_competitor(req.competitor_name, req.website, req.context)
    )


class TenderRequest(BaseModel):
    product_category: str
    region: str


@app.post("/atlas/tenders", response_model=AgentResponse, tags=["ATLAS"])
async def find_tenders(req: TenderRequest, token: str = Security(_verify_token)):
    agent = AtlasResearchAgent()
    return AgentResponse(
        agent="ATLAS",
        result=agent.find_tenders(req.product_category, req.region)
    )


class CountryResearchRequest(BaseModel):
    country: str


@app.post("/atlas/country", response_model=AgentResponse, tags=["ATLAS"])
async def research_country(req: CountryResearchRequest, token: str = Security(_verify_token)):
    agent = AtlasResearchAgent()
    return AgentResponse(
        agent="ATLAS",
        result=agent.research_country_market(req.country)
    )


# ── NOVA Endpoints ───────────────────────────────────────────────────────────

@app.post("/nova/weekly-report", response_model=AgentResponse, tags=["NOVA"])
async def weekly_report(req: TaskRequest, token: str = Security(_verify_token)):
    agent = NovaAnalyticsAgent()
    return AgentResponse(
        agent="NOVA",
        result=agent.weekly_ceo_report(req.context)
    )


@app.post("/nova/kpi-framework", response_model=AgentResponse, tags=["NOVA"])
async def build_kpi_framework(token: str = Security(_verify_token)):
    agent = NovaAnalyticsAgent()
    return AgentResponse(
        agent="NOVA",
        result=agent.build_kpi_framework()
    )


# ── Health Check ─────────────────────────────────────────────────────────────

@app.get("/health")
async def health_check():
    return {
        "status": "running",
        "employees": ["AMARA", "CHISOM", "KOFI", "ZARA", "EMEKA", "FATIMA", "ATLAS", "NOVA"],
        "scheduled_jobs": [job.id for job in scheduler.get_jobs()],
    }
