# Testing Frontend & Backend (Gemini, Slack, Tasks, Calendar)

## Quick test (backend only)

1. **Start the backend** (use port 8001 if 8000 is already in use):
   ```bash
   cd backend
   # Ensure .env has GEMINI_API_KEY, WEBHOOK_URL_SLACK_TASKS, WEBHOOK_URL_SLACK_AGENT
   python -m uvicorn app:app --host 127.0.0.1 --port 8001
   ```

2. **Run the E2E script** (same machine):
   ```bash
   cd backend
   API_BASE=http://127.0.0.1:8001 python test_e2e.py
   ```

   Expected:
   - **GET /health** → `status: ok`, `service: agentic-task-api`
   - **POST /api/tasks** → creates task, sends to Slack **#samayak-project-tasks**
   - **GET /api/tasks** → list of tasks
   - **POST /api/agent/process** → Gemini response, sends breakdown to Slack **#samyak**
   - **GET /api/productivity/report** → metrics
   - **PATCH /api/tasks/{id}** status=completed → sends to **#samayak-project-tasks**

## Full stack (frontend + backend)

1. **Backend** (terminal 1):
   ```bash
   cd backend
   python -m uvicorn app:app --host 0.0.0.0 --port 8000
   ```
   If port 8000 is in use, use `--port 8001` and set frontend `.env.local`:  
   `NEXT_PUBLIC_API_URL=http://localhost:8001`

2. **Frontend** (terminal 2):
   ```bash
   pnpm dev
   # or: npm run dev
   ```
   Open http://localhost:3000

3. **Manual checks**
   - **Landing** → Open dashboard, Tasks & Hours, Voice Agent.
   - **Tasks** → Create a task; it should appear and (if Slack webhooks set) post to **#samayak-project-tasks**.
   - **Voice Agent** → Send a message (e.g. “Break down the task: Review PR by Friday”); response from Gemini and (if Slack set) breakdown in **#samyak**.
   - **Productivity** → Tasks & Hours → Productivity tab; see report.

## Slack

- **#samayak-project-tasks**: Task created / updated / completed (from `notify_task_event`).
- **#samyak**: Agent breakdown after each `/api/agent/process` (from `notify_agent_breakdown`).

Set in `backend/.env`:
- `WEBHOOK_URL_SLACK_TASKS=...`
- `WEBHOOK_URL_SLACK_AGENT=...`

## Gemini

- Set `GEMINI_API_KEY=...` in `backend/.env`.
- Agent uses it in `utils/gemini_adapter.py`; orchestrator in `agent/orchestrator.py`.

## Calendar

- **Google OAuth client** is configured (`GOOGLE_OAUTH_CLIENT_ID` in `backend/.env`) for Gmail/Calendar.
- **Calendar hook** (e.g. “when someone sends a task, add to Google Calendar”) is not implemented yet; use the OAuth client when you add that flow.

## Troubleshooting

- **Agent returns 500** `'function' object has no attribute 'completions'`: fixed by making `GeminiClient.chat` a property in `utils/gemini_adapter.py`. Restart backend.
- **Agent times out**: Increase timeout in `test_e2e.py` or wait longer; ensure `GEMINI_API_KEY` is set.
- **Slack not receiving**: Check `WEBHOOK_URL_SLACK_TASKS` and `WEBHOOK_URL_SLACK_AGENT`; URLs must be exact (no trailing slash).
- **Frontend can’t reach backend**: Ensure `NEXT_PUBLIC_API_URL` matches backend host/port and CORS allows the frontend origin.
