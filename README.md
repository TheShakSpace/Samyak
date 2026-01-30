# Samyak

**Agentic Task & Management** – Remote team task and productivity tracker with an AI voice agent.

## Features

- **Tasks** – Create, assign, and track tasks with status and priority
- **Working hours** – Log and view hours per task/user
- **Productivity reports** – Completion rates and time insights
- **Voice Agent** – Chat, generate docs, and get strategy via Gemini
- **Notifications** – Slack/Discord/Teams webhooks for task events

## Tech stack

| Layer   | Stack                    |
|---------|--------------------------|
| Frontend | Next.js, React           |
| Backend  | FastAPI, Python          |
| AI       | Google Gemini            |
| DB       | Firebase Firestore (opt) |

## Quick start

**1. Backend** (port 8000)

```bash
cd backend
pip install -r requirements.txt
cp env.example .env   # add GEMINI_API_KEY, etc.
python -m uvicorn app:app --port 8000
```

**2. Frontend** (port 3000)

```bash
pnpm install   # or npm install
pnpm dev       # or npm run dev
```

**3. Open** [http://localhost:3000](http://localhost:3000)

## Environment

- **Backend:** `backend/.env` – copy from `backend/env.example` (Gemini, Firebase, Slack webhooks, SMTP).
- **Frontend:** `.env.local` – copy from `env.local.example` (Firebase web config if using Firebase Auth).

See [docs/ENV_VARIABLES.md](docs/ENV_VARIABLES.md) and [docs/CREDENTIALS_CHECKLIST.md](docs/CREDENTIALS_CHECKLIST.md) for details.

## Docs

| Doc | Description |
|-----|-------------|
| [docs/CONVERSION_PLAN.md](docs/CONVERSION_PLAN.md) | Architecture and phases |
| [docs/TESTING.md](docs/TESTING.md) | Run backend, frontend, and E2E |
| [docs/CREDENTIALS_CHECKLIST.md](docs/CREDENTIALS_CHECKLIST.md) | API keys and OAuth setup |

## License

MIT
