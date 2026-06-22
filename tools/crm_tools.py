"""
CRM — Lightweight SQLModel-based customer relationship management.
Tracks leads, customers, interactions, and pipeline stages.
"""

from __future__ import annotations

import os
from datetime import datetime
from enum import Enum
from typing import Optional

from sqlmodel import Field, Session, SQLModel, create_engine, select


class LeadTier(str, Enum):
    A = "A"
    B = "B"
    C = "C"


class LeadStatus(str, Enum):
    NEW = "new"
    CONTACTED = "contacted"
    RESPONDED = "responded"
    QUALIFIED = "qualified"
    OPPORTUNITY = "opportunity"
    CLOSED_WON = "closed_won"
    CLOSED_LOST = "closed_lost"


class CustomerSegment(str, Enum):
    CHAMPION = "A_champion"
    LOYAL = "B_loyal"
    POTENTIAL = "C_potential"
    AT_RISK = "D_at_risk"
    LOST = "E_lost"


class Lead(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    company: str
    contact_name: str
    title: str = ""
    email: str = ""
    phone: str = ""
    whatsapp: str = ""
    country: str
    segment: str = ""
    tier: LeadTier = LeadTier.C
    status: LeadStatus = LeadStatus.NEW
    source: str = ""
    notes: str = ""
    last_contact: Optional[datetime] = None
    next_action: str = ""
    next_action_date: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Customer(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    company: str
    contact_name: str
    email: str = ""
    whatsapp: str = ""
    country: str
    segment: CustomerSegment = CustomerSegment.POTENTIAL
    total_orders: int = 0
    total_revenue_usd: float = 0.0
    first_order_date: Optional[datetime] = None
    last_order_date: Optional[datetime] = None
    preferred_products: str = ""
    notes: str = ""
    nps_score: Optional[int] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Interaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    entity_type: str  # "lead" or "customer"
    entity_id: int
    channel: str  # email, whatsapp, phone, social
    direction: str  # inbound, outbound
    content: str = ""
    agent: str = ""  # which AI employee handled it
    outcome: str = ""
    created_at: datetime = Field(default_factory=datetime.utcnow)


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./opes_employees.db")
engine = create_engine(DATABASE_URL, echo=False)


def init_db() -> None:
    SQLModel.metadata.create_all(engine)


class CRMTools:
    def __init__(self) -> None:
        init_db()

    # ── Lead Operations ─────────────────────────────────────────────────────

    def create_lead(self, **kwargs) -> Lead:
        lead = Lead(**kwargs)
        with Session(engine) as s:
            s.add(lead)
            s.commit()
            s.refresh(lead)
        return lead

    def update_lead(self, lead_id: int, **kwargs) -> Lead | None:
        with Session(engine) as s:
            lead = s.get(Lead, lead_id)
            if not lead:
                return None
            for k, v in kwargs.items():
                setattr(lead, k, v)
            lead.updated_at = datetime.utcnow()
            s.add(lead)
            s.commit()
            s.refresh(lead)
        return lead

    def get_leads_by_status(self, status: LeadStatus) -> list[Lead]:
        with Session(engine) as s:
            return s.exec(select(Lead).where(Lead.status == status)).all()

    def get_hot_leads(self) -> list[Lead]:
        with Session(engine) as s:
            return s.exec(
                select(Lead).where(Lead.tier == LeadTier.A, Lead.status == LeadStatus.QUALIFIED)
            ).all()

    # ── Customer Operations ─────────────────────────────────────────────────

    def create_customer(self, **kwargs) -> Customer:
        customer = Customer(**kwargs)
        with Session(engine) as s:
            s.add(customer)
            s.commit()
            s.refresh(customer)
        return customer

    def update_customer(self, customer_id: int, **kwargs) -> Customer | None:
        with Session(engine) as s:
            c = s.get(Customer, customer_id)
            if not c:
                return None
            for k, v in kwargs.items():
                setattr(c, k, v)
            c.updated_at = datetime.utcnow()
            s.add(c)
            s.commit()
            s.refresh(c)
        return c

    def get_at_risk_customers(self, inactive_days: int = 90) -> list[Customer]:
        from datetime import timedelta
        cutoff = datetime.utcnow() - timedelta(days=inactive_days)
        with Session(engine) as s:
            return s.exec(
                select(Customer).where(Customer.last_order_date < cutoff)
            ).all()

    def get_customers_by_segment(self, segment: CustomerSegment) -> list[Customer]:
        with Session(engine) as s:
            return s.exec(select(Customer).where(Customer.segment == segment)).all()

    # ── Interaction Logging ─────────────────────────────────────────────────

    def log_interaction(self, **kwargs) -> Interaction:
        interaction = Interaction(**kwargs)
        with Session(engine) as s:
            s.add(interaction)
            s.commit()
            s.refresh(interaction)
        return interaction

    # ── Reporting ───────────────────────────────────────────────────────────

    def pipeline_summary(self) -> dict:
        with Session(engine) as s:
            summary = {}
            for status in LeadStatus:
                count = len(s.exec(select(Lead).where(Lead.status == status)).all())
                summary[status.value] = count
        return summary

    def revenue_by_country(self) -> dict[str, float]:
        with Session(engine) as s:
            customers = s.exec(select(Customer)).all()
        result: dict[str, float] = {}
        for c in customers:
            result[c.country] = result.get(c.country, 0.0) + c.total_revenue_usd
        return dict(sorted(result.items(), key=lambda x: x[1], reverse=True))
