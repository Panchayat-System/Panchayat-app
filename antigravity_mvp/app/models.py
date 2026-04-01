from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Literal


class WhatsAppMessage(BaseModel):
    resident_id: str
    text: str = Field(min_length=1)
    channel: Literal["whatsapp"] = "whatsapp"
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class DramaFilterRequest(BaseModel):
    messages: List[str] = Field(default_factory=list)


class IssueCluster(BaseModel):
    topic: str
    mentions: int
    sentiment: Literal["negative", "neutral", "positive"]
    summary: str


class DramaFilterResponse(BaseModel):
    actionable_summary: List[str]
    clusters: List[IssueCluster]


class VoiceTicketRequest(BaseModel):
    resident_id: str
    transcript: str = Field(min_length=2)
    language: str = "auto"


class Ticket(BaseModel):
    id: str
    resident_id: str
    category: str
    priority: Literal["low", "medium", "high"]
    description: str
    assigned_to: str
    status: Literal["open", "in_progress", "closed"] = "open"
    created_at: datetime = Field(default_factory=datetime.utcnow)


class WeeklyDashboard(BaseModel):
    total_messages: int
    total_tickets: int
    open_tickets: int
    closed_tickets: int
    recurring_topics: List[str]
