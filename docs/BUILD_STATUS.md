# Build Status – Agentic Task & Management

## Done

- **Phase 1:** Config for Gemini, Firebase, webhooks (`backend/config.py`, `backend/env.example`, `env.local.example`, `docs/ENV_VARIABLES.md`).
- **Phase 2:** Firebase data layer: `backend/db/firebase.py` (Firestore TaskManager + HoursRepository), `backend/models/working_hours.py`, `backend/db/factory.py` (JSON vs Firestore switch).
- **Phase 3:** Gemini adapter `backend/utils/gemini_adapter.py`; orchestrator uses Gemini (and optional Llama/OpenAI fallback).
- **Phase 4:** `backend/tools/hours_tools.py` (log/get working hours), productivity report includes hours when Firebase is used; `backend/utils/webhooks.py` for optional Slack/Discord/Teams.
- **Phase 5:** FastAPI server `backend/app.py`: REST API for tasks, working-hours, productivity report, agent process; CORS for frontend.
- **Phase 6:** Frontend: `lib/tasks-api.ts` (tasks, hours, productivity, agent); `lib/ai-service.ts` calls backend `/api/agent/process`; dashboard sidebar "Voice Agent" / "Tasks & Hours"; `components/tasks-productivity-view.tsx` (tasks list, log hours, productivity report).

## How to run

### Backend (FastAPI)

```bash
cd backend
cp env.example .env
# Edit .env: set GEMINI_API_KEY (required for agent). Optionally USE_FIREBASE=true and GOOGLE_APPLICATION_CREDENTIALS for Firestore.
pip install -r requirements.txt
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

Without Firebase: tasks use JSON file (`data/tasks.json`). Working hours endpoints return "not available" unless Firebase is configured.

### Frontend (Next.js)

```bash
cp env.local.example .env.local
# Set NEXT_PUBLIC_API_URL=http://localhost:8000
pnpm install
pnpm dev
```

Open the dashboard; use **Voice Agent** for chat (backend agent + Gemini) and **Tasks & Hours** for tasks, log hours, and productivity report.

## Optional

- **Firebase:** Set `USE_FIREBASE=true` and `GOOGLE_APPLICATION_CREDENTIALS` to your service account JSON path. Create Firestore collections `tasks` and `working_hours` (they are created on first write).
- **Webhooks:** Set `WEBHOOK_URL_SLACK` or `WEBHOOK_URL_DISCORD` in `.env` for task event notifications.
- **Visualization tools:** Install `matplotlib` and `pandas` for chart tools in the agent (optional).
