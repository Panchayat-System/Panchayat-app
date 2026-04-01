from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.models import VoiceTicketRequest
from app.services import create_ticket_from_voice, summarize_messages


def test_drama_filter_clusters_lift_and_gym():
    res = summarize_messages([
        "Lift not working since morning",
        "Please fix elevator",
        "Can we change gym timing?",
    ])
    topics = [c.topic for c in res.clusters]
    assert "Lift issue" in topics
    assert "Gym timing request" in topics


def test_voice_to_ticket_plumbing_classification():
    ticket = create_ticket_from_voice(
        VoiceTicketRequest(
            resident_id="R-10",
            transcript="Tap leak ho raha hai kitchen me",
            language="hi",
        )
    )
    assert ticket.category == "Plumbing"
    assert ticket.priority == "medium"
