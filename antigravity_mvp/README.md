# Panchayat AI — WhatsApp-first MVP ("Antigravity")

This is a fast-start MVP scaffold for an apartment-society assistant focused on:

1. **Drama Filter** (message summarization + clustering)
2. **Voice-to-Ticket** (transcribed text to structured ticket)
3. **Basic Dashboard** (weekly operational metrics)

## Why this architecture

The project is intentionally small and practical for pilot societies:

- **FastAPI backend** for webhook + API endpoints
- **In-memory store** for speed (replace with Postgres later)
- **Rule-based NLP stubs** so you can run today without model keys
- **Pluggable AI layer** to add OpenAI/other models later

## Quick start

```bash
cd antigravity_mvp
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Open docs at: `http://localhost:8000/docs`

## Suggested first pilot flow

1. POST WhatsApp text messages to `/whatsapp/webhook`
2. Call `/drama-filter/summary` for action digest
3. POST voice transcript to `/tickets/from-voice`
4. View `/dashboard/weekly`

## Next production upgrades

- Replace `InMemoryStore` with Postgres + Redis.
- Add background jobs (Celery/RQ) for summarization batches.
- Integrate official WhatsApp Business API provider.
- Add auth, tenant isolation, audit logs, and SLA engine.
