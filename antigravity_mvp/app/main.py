from fastapi import FastAPI

from .models import DramaFilterRequest, DramaFilterResponse, VoiceTicketRequest, Ticket, WeeklyDashboard, WhatsAppMessage
from .services import create_ticket_from_voice, summarize_messages, weekly_dashboard
from .store import store

app = FastAPI(title="Panchayat AI MVP", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/whatsapp/webhook")
def whatsapp_webhook(message: WhatsAppMessage) -> dict[str, str]:
    store.add_message(message)
    return {"message": "received"}


@app.post("/drama-filter/summary", response_model=DramaFilterResponse)
def drama_filter_summary(payload: DramaFilterRequest) -> DramaFilterResponse:
    return summarize_messages(payload.messages)


@app.post("/tickets/from-voice", response_model=Ticket)
def ticket_from_voice(payload: VoiceTicketRequest) -> Ticket:
    return create_ticket_from_voice(payload)


@app.get("/dashboard/weekly", response_model=WeeklyDashboard)
def dashboard_weekly() -> WeeklyDashboard:
    return weekly_dashboard()
