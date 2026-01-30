# Samyak

Agentic Task & Management – Remote Team Task and Productivity Tracker.

- **Frontend:** Next.js dashboard (tasks, Voice Agent, productivity).
- **Backend:** FastAPI (tasks, working hours, Gemini agent, Slack webhooks).
- **Docs:** See `docs/` for setup, credentials, and testing.

## Quick start

```bash
# Backend
cd backend && pip install -r requirements.txt && python -m uvicorn app:app --port 8000

# Frontend
pnpm install && pnpm dev
```

Open http://localhost:3000. Set `GEMINI_API_KEY` in `backend/.env` for live AI.
