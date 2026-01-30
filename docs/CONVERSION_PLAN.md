# Agentic Task & Management – Conversion Plan

## Remote Team Task and Productivity Tracker

**Goal:** Convert the current project into a task management platform for remote teams with assign work, track productivity, role-based dashboards, and AI-powered agents using **Gemini** (replacing Ollama). Use **Firebase** in the **backend only** for persistence; connect the existing dashboard to the new backend.

---

## Current State Summary

| Area | Current | Target |
|------|--------|--------|
| **LLM** | Llama (Ollama) / optional OpenAI | **Gemini** only |
| **Storage** | JSON file (`data/tasks.json`) | **Firebase Firestore** (backend only) |
| **Backend API** | None (CLI/tools only) | **FastAPI** server with REST + webhooks |
| **Frontend** | Next.js dashboard + Agent Room (Vittya-style) | Same dashboard **wired to backend**; task management + productivity features |
| **Agents** | `TaskManagementAgent`, `RequestRouter`, task/email/query/visualization tools | **Reuse** these agents; add Gemini adapter; add working-hours & report tools |

---

## Features to Deliver

1. **Create and assign tasks** – CRUD tasks, assign to team members (by user/email).
2. **Track task status** – todo / in_progress / completed with history.
3. **Log working hours** – time entries per task (and optionally per user).
4. **Role-based dashboards** – views for Admin, Manager, Member (and optionally Guest).
5. **Generate productivity reports** – completion rates, hours logged, assignee/team summaries (agent + API).
6. **AI agents** – Use existing orchestrator + router + tools; switch to **Gemini**; keep backend-only Firebase.

---

## Plan & Phases

### Phase 1: Environment & Configuration

**Objective:** Centralize all credentials and webhooks in env; no secrets in code.

**Tasks:**

1. **Backend `.env` and `.env.example`**
   - `GEMINI_API_KEY` – Gemini API key.
   - `GOOGLE_APPLICATION_CREDENTIALS` or Firebase service-account JSON path for backend-only Firebase.
   - Firebase project ID / config if needed by Admin SDK.
   - `WEBHOOK_URL_*` – e.g. Slack/Discord/Teams for notifications (optional).
   - SMTP for email (existing): `SMTP_SERVER`, `SMTP_PORT`, `EMAIL_ADDRESS`, `EMAIL_PASSWORD`.
   - Backend base URL for webhooks: `BACKEND_BASE_URL` (e.g. `http://localhost:8000`).
   - Optional: `OPENAI_API_KEY` only if keeping a fallback (otherwise remove).

2. **Frontend `.env.local.example`**
   - `NEXT_PUBLIC_API_URL` – Backend API base (e.g. `http://localhost:8000`).
   - No Firebase keys in frontend (backend-only Firebase).

3. **Documentation**
   - Add a short “Environment variables” section in README or SETUP pointing to `.env.example` and `.env.local.example`.

**Deliverables:**  
- `backend/env.example` (copy to `backend/.env`)  
- `env.local.example` at repo root (copy to `.env.local` for Next.js)  
- `docs/ENV_VARIABLES.md`

---

### Phase 2: Backend – Firebase & Data Layer

**Objective:** Replace JSON file with Firebase (backend only). Keep existing `Task` model semantics; add `WorkingHours` (and optionally `User`/roles).

**Tasks:**

1. **Firebase setup (backend only)**
   - Create Firebase project; get service account JSON.
   - Use Firestore (and optionally Auth for “backend-verified” user IDs later).
   - Put credentials path in `GOOGLE_APPLICATION_CREDENTIALS` or load from env.

2. **Firestore collections (design)**
   - `tasks` – same fields as current `Task` (task_id, title, description, priority, deadline, status, assignee, tags, created_at, updated_at, completed_at). Use `assignee` as email or uid.
   - `working_hours` – id, task_id, user_id/email, minutes (or start/end), date, notes.
   - Optional: `users` or `teams` for role (admin/manager/member) – or derive role from a fixed list / Firebase Custom Claims later.

3. **Backend data layer**
   - New module: `backend/db/` or `backend/services/firebase.py` – init Firestore, wrappers for:
     - Tasks: create, get, update, delete, list (with filters: assignee, status, priority, tag).
     - Working hours: log, list by task, list by user, list by date range.
   - New `TaskManager` (or `TaskRepository`) that uses Firestore instead of JSON; keep same method names where possible so existing `task_tools` can be switched to it.
   - Keep `models/task.py` `Task` and `from_dict`/`to_dict`; add `WorkingHours` model and repository.

**Deliverables:**  
- `backend/db/firebase.py` (or `backend/services/firebase.py`)  
- `backend/models/working_hours.py` (optional separate file or in `task.py`)  
- `TaskManager` backed by Firestore  
- Backend reads/writes only from Firebase (no `data/tasks.json` in code paths)

---

### Phase 3: Backend – Gemini Adapter & Agent Wiring

**Objective:** Replace Llama/Ollama (and optional OpenAI) with Gemini. Existing agents and tools remain; only the LLM client changes.

**Tasks:**

1. **Gemini adapter**
   - New file: `backend/utils/gemini_adapter.py` (or `backend/llm/gemini_client.py`).
   - Implement same interface as current LLM usage in `agent/orchestrator.py`: e.g. “chat with system + user messages, optional tools”.
   - Use Google’s Gemini API (REST or SDK) with `GEMINI_API_KEY`.
   - Map existing “tools” (create_task, update_task_status, …) to Gemini function calling if supported; otherwise keep “prompt + tool list” and parse agent response to call tools (current pattern).

2. **Config**
   - In `config.py`: remove or deprecate `LLAMA_*`, `LLM_PROVIDER=llama`; add `LLM_PROVIDER=gemini`, `GEMINI_API_KEY`, `GEMINI_MODEL` (e.g. `gemini-1.5-flash` or `gemini-1.5-pro`).

3. **Orchestrator**
   - In `agent/orchestrator.py`: replace Llama client with Gemini adapter; keep `RequestRouter`, tool registration, and `process_request` flow. Ensure tool calls (create_task, update_task_status, get_all_tasks, etc.) use the new Firestore-backed TaskManager.

**Deliverables:**  
- `backend/utils/gemini_adapter.py`  
- `config.py` updated for Gemini  
- `agent/orchestrator.py` using Gemini and existing tools

---

### Phase 4: Backend – Working Hours & Productivity Reports

**Objective:** Support “log working hours” and “generate productivity reports” in backend and for agents.

**Tasks:**

1. **Working hours**
   - New tools (e.g. in `tools/hours_tools.py`): `log_working_hours(task_id, user_id_or_email, minutes, date, notes)`, `get_working_hours(task_id=None, user_id=None, from_date, to_date)`.
   - Register these in the orchestrator so the agent can “log hours” and “report hours” from natural language.

2. **Productivity reports**
   - Extend or add tool: `generate_productivity_report(assignee=None, from_date, to_date)` – aggregate tasks completed, completion rate, total hours logged (from `working_hours`), optional breakdown by priority/status.
   - Existing `calculate_productivity_metrics` can be adapted to read from Firestore and include hours; or call it from a new “report” tool that also pulls working hours.

3. **Optional webhooks**
   - On task created/updated/completed, call configurable `WEBHOOK_URL_*` (e.g. Slack) with a small JSON payload. Env-driven; no webhook URL in code.

**Deliverables:**  
- `tools/hours_tools.py`  
- Productivity report tool (or extended `calculate_productivity_metrics`)  
- Optional webhook on task events (env-based URL)

---

### Phase 5: Backend – FastAPI Server & REST API

**Objective:** Expose a single backend so the dashboard can create/assign tasks, track status, log hours, and get productivity data. Same backend will also serve the agent (e.g. “process natural language request”).

**Tasks:**

1. **FastAPI app**
   - New file: `backend/app.py` or `backend/main_api.py` – create FastAPI app, CORS for frontend origin, mount routes.

2. **Auth (minimal for dashboard)**
   - Option A: Keep using your existing auth (e.g. Firebase Auth or custom) and have frontend send `Authorization: Bearer <token>`; backend verifies token and extracts `uid`/email for “current user” and role.
   - Option B: For MVP, use a simple API key or session header for dashboard; add proper JWT/Firebase later.
   - Document: “Role” can come from token claims or a small `users` table in Firestore (admin/manager/member).

3. **REST endpoints**
   - **Tasks:**  
     - `POST /api/tasks` – create task (body: title, description, priority, deadline, assignee, tags).  
     - `GET /api/tasks` – list tasks (query: status, assignee, priority, tag).  
     - `GET /api/tasks/{task_id}` – get one task.  
     - `PATCH /api/tasks/{task_id}` – update (e.g. status, assignee).  
     - `DELETE /api/tasks/{task_id}` – delete.
   - **Working hours:**  
     - `POST /api/working-hours` – log (task_id, user_id/email, minutes, date, notes).  
     - `GET /api/working-hours` – list (task_id, user_id, from_date, to_date).
   - **Productivity:**  
     - `GET /api/productivity/report` – query params: assignee, from_date, to_date; return JSON (completion rate, hours, tasks breakdown).
   - **Agent:**  
     - `POST /api/agent/process` – body: `{ "request": "natural language string" }`; return agent response (and optionally tool-used summary). Uses existing orchestrator + Gemini + tools.

4. **Webhooks (optional)**
   - If implemented in Phase 4, ensure env vars are read in app startup and documented in `.env.example`.

**Deliverables:**  
- `backend/app.py` (or `main_api.py`)  
- REST routes for tasks, working-hours, productivity report, agent  
- CORS and auth strategy documented

---

### Phase 6: Frontend – Connect Dashboard to Backend

**Objective:** Dashboard and Agent Room use the real backend: tasks, hours, productivity, and agent.

**Tasks:**

1. **API client**
   - Extend `lib/api.ts` (or add `lib/tasks-api.ts`):  
     - `getTasks(params)`, `getTask(id)`, `createTask(payload)`, `updateTask(id, payload)`, `deleteTask(id)`.  
     - `logWorkingHours(payload)`, `getWorkingHours(params)`.  
     - `getProductivityReport(params)`.  
     - `processAgentRequest(request)` – POST to `/api/agent/process`.  
   - Use `NEXT_PUBLIC_API_URL` and send auth header (e.g. Bearer token from existing auth context).

2. **Agent Room**
   - Replace or extend `lib/ai-service.ts` so that:
     - `chat(messages, trainingData)` calls backend `POST /api/agent/process` with the last user message (and optionally history), returns response text (Gemini via backend).
     - Keep existing UI; only the data source changes from mock to backend.
   - Optional: keep `analyzeUploadedData`, `generateFinanceDocument`, `generateFinanceStrategy` as backend endpoints later, or stub to agent “analyze this / generate document / generate strategy” so one agent handles all.

3. **Dashboard pages**
   - **Tasks:** A tasks list page (or section) that uses `getTasks` / `createTask` / `updateTask` / `deleteTask` – table or cards with status, assignee, priority, due date; create/edit modal or inline.
   - **Working hours:** A form or section to log time (task picker, minutes, date) calling `logWorkingHours`; optional list of “my hours” or “hours for this task”.
   - **Productivity:** A simple report view that calls `getProductivityReport` and shows completion rate, hours, maybe a small chart (reuse existing chart components if any).

**Deliverables:**  
- Updated `lib/api.ts` and/or `lib/tasks-api.ts`  
- `lib/ai-service.ts` calling backend agent  
- Dashboard: Tasks UI, Log hours UI, Productivity report UI

---

### Phase 7: Role-Based Dashboards

**Objective:** Show different nav and content by role (Admin, Manager, Member).

**Tasks:**

1. **Backend**
   - Ensure `/api/productivity/report` and task list can be filtered by “current user” or “team”; Admin can see all, Manager can see team, Member sees own.
   - If using Firebase Auth, store role in Custom Claims or a `users` collection (e.g. `role: admin | manager | member`). Backend reads role from token or from Firestore by uid.

2. **Frontend**
   - Get role from auth context (or from a small `/api/me` that returns `{ uid, email, role }`).
   - Sidebar/nav: show “Tasks”, “My hours”, “Productivity” for all; add “Team report” or “All tasks” for Manager; add “Admin” (user management, full reports) for Admin.
   - Each dashboard view already uses the API; no change to API contract, only to what’s visible and what filters are applied (e.g. assignee=me vs no filter).

**Deliverables:**  
- Role stored and returned (e.g. `/api/me` or token claims)  
- Dashboard nav and visibility by role

---

### Phase 8: Polish & Documentation

**Objective:** Env documented, README updated, optional webhooks and credentials clearly listed.

**Tasks:**

1. **Env**
   - Finalize `backend/.env.example` and `.env.local.example` with every variable needed: Gemini, Firebase, SMTP, webhooks, `BACKEND_BASE_URL`, `NEXT_PUBLIC_API_URL`.
2. **README**
   - Short “Remote Team Task & Productivity Tracker” description; how to run backend (uvicorn), frontend (pnpm dev); env setup; Firebase and Gemini one-time setup.
3. **Optional**
   - Docker Compose for backend + frontend if desired.

**Deliverables:**  
- Updated README  
- `docs/ENV_VARIABLES.md` or equivalent section in SETUP

---

## Dependency Order

- Phase 1 (env) first.  
- Phase 2 (Firebase) before Phase 3 (Gemini + tools), because tools will use Firestore.  
- Phase 3 and 4 can overlap once Firebase is in place.  
- Phase 5 (FastAPI) after 2–4 so routes use Firebase and agent.  
- Phase 6 (frontend) after Phase 5.  
- Phase 7 (roles) after 6.  
- Phase 8 anytime; refine in parallel.

---

## Agents to Reuse (No Rewrite)

- **`agent/router.py`** – `RequestRouter`: categorize request, recommend tools.  
- **`agent/orchestrator.py`** – `TaskManagementAgent`: register tools, `process_request`, system prompt.  
- **`tools/task_tools.py`** – create_task, update_task_status, get_tasks_by_priority, get_all_tasks, delete_task, calculate_productivity_metrics.  
- **`tools/email_tools.py`** – send_task_reminder, send_productivity_summary, etc.  
- **`tools/query_tools.py`** – query_tasks_with_code.  
- **`tools/visualization_tools.py`** – charts (optional for reports).

**Changes:**  
- Swap LLM in orchestrator to Gemini.  
- Swap `TaskManager` implementation to Firestore in `task_tools` (and config).  
- Add `hours_tools` and wire productivity report to working hours.

---

## Backend–Dashboard Linking

- **Dashboard** (Next.js) calls **one backend** via `NEXT_PUBLIC_API_URL` (e.g. `http://localhost:8000`).
- **REST API:** Tasks CRUD, working hours log/list, productivity report, agent process. Frontend uses `lib/api.ts` (and optional `lib/tasks-api.ts`) with `Authorization: Bearer <token>` if auth is enabled.
- **Agent Room:** Chat and “process request” go to `POST /api/agent/process`; `lib/ai-service.ts` is updated to call this instead of mock.
- **Auth:** Existing auth context (e.g. Firebase Auth or custom) can stay; backend validates token and uses `uid`/email for “current user” and role-based filters.

## Firebase (Backend Only)

- Frontend does **not** import Firebase SDK for Firestore.  
- All Firestore access is in the backend (FastAPI + agents).  
- Frontend talks to backend only via REST; auth can stay Firebase Auth (tokens) or your current auth; backend verifies token and uses Firebase Admin SDK for DB.

---

## Summary Table

| Phase | Focus | Key deliverables |
|-------|--------|-------------------|
| 1 | Env & config | `.env.example` (backend + frontend), docs |
| 2 | Firebase & data | Firestore collections, TaskManager + WorkingHours repo |
| 3 | Gemini & agents | Gemini adapter, orchestrator wired to Gemini + Firestore |
| 4 | Hours & reports | hours_tools, productivity report tool, optional webhooks |
| 5 | FastAPI | REST API: tasks, working-hours, productivity, agent |
| 6 | Dashboard link | api client, Agent Room → backend, Tasks/Hours/Report UI |
| 7 | Roles | Role-based nav and visibility |
| 8 | Polish | README, env docs |

You can implement in this order and track progress per phase.

---

## Build status

Implementation is in place for Phases 1–6. See `docs/BUILD_STATUS.md` for what’s done and how to run backend and frontend.
