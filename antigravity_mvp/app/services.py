from __future__ import annotations

from collections import Counter
from uuid import uuid4

from .models import DramaFilterResponse, IssueCluster, Ticket, VoiceTicketRequest, WeeklyDashboard
from .store import store


TOPIC_KEYWORDS = {
    "lift": "Lift issue",
    "elevator": "Lift issue",
    "gym": "Gym timing request",
    "water": "Water supply",
    "leak": "Plumbing leak",
    "tap": "Plumbing leak",
    "security": "Security concern",
    "parking": "Parking management",
}


def summarize_messages(messages: list[str]) -> DramaFilterResponse:
    if not messages:
        return DramaFilterResponse(actionable_summary=[], clusters=[])

    topic_counter: Counter[str] = Counter()
    for message in messages:
        text = message.lower()
        matched = False
        for key, topic in TOPIC_KEYWORDS.items():
            if key in text:
                topic_counter[topic] += 1
                matched = True
        if not matched:
            topic_counter["General discussion"] += 1

    clusters = [
        IssueCluster(
            topic=topic,
            mentions=count,
            sentiment="negative" if "issue" in topic.lower() or "leak" in topic.lower() else "neutral",
            summary=f"{topic} raised by {count} residents/messages.",
        )
        for topic, count in topic_counter.most_common(5)
    ]

    actionable = [cluster.summary for cluster in clusters]
    return DramaFilterResponse(actionable_summary=actionable, clusters=clusters)


def create_ticket_from_voice(req: VoiceTicketRequest) -> Ticket:
    text = req.transcript.lower()

    if any(word in text for word in ["leak", "tap", "pipe", "kitchen"]):
        category = "Plumbing"
        assigned_to = "Vendor-Plumbing"
        priority = "medium"
    elif any(word in text for word in ["lift", "elevator", "stuck"]):
        category = "Lift"
        assigned_to = "Vendor-Lift"
        priority = "high"
    elif any(word in text for word in ["security", "guard", "gate"]):
        category = "Security"
        assigned_to = "Security-Supervisor"
        priority = "high"
    else:
        category = "General"
        assigned_to = "Society-Manager"
        priority = "low"

    ticket = Ticket(
        id=f"TKT-{uuid4().hex[:8].upper()}",
        resident_id=req.resident_id,
        category=category,
        priority=priority,
        description=req.transcript,
        assigned_to=assigned_to,
    )
    store.add_ticket(ticket)
    return ticket


def weekly_dashboard() -> WeeklyDashboard:
    total_messages = len(store.messages)
    total_tickets = len(store.tickets)
    closed_tickets = len([t for t in store.tickets if t.status == "closed"])
    open_tickets = total_tickets - closed_tickets

    recurrences = summarize_messages([m.text for m in store.messages]).clusters
    recurring_topics = [cluster.topic for cluster in recurrences]

    return WeeklyDashboard(
        total_messages=total_messages,
        total_tickets=total_tickets,
        open_tickets=open_tickets,
        closed_tickets=closed_tickets,
        recurring_topics=recurring_topics,
    )
