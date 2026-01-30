# Environment Variables

Reference for all credentials and configuration used by the **Agentic Task & Management** (Remote Team Productivity) app.

---

## Backend (`backend/.env`)

Copy from `backend/env.example` to `backend/.env`. Required for running the FastAPI server and agents.

| Variable | Required | Description |
|----------|----------|-------------|
| `GEMINI_API_KEY` | Yes | Google Gemini API key ([Google AI Studio](https://aistudio.google.com/)). |
| `GEMINI_MODEL` | No | Model name, e.g. `gemini-1.5-flash` or `gemini-1.5-pro`. Default: `gemini-1.5-flash`. |
| `GOOGLE_APPLICATION_CREDENTIALS` | Yes | Path to Firebase service account JSON (Firestore, backend only). |
| `FIREBASE_PROJECT_ID` | No | Override project ID; otherwise read from service account JSON. |
| `BACKEND_BASE_URL` | No | Base URL of this backend (e.g. `http://localhost:8000`). Used for webhook callbacks. |
| `WEBHOOK_URL_SLACK_TASKS` | No | Slack webhook for **#samayak-project-tasks** (task assignments: created/updated/completed). |
| `WEBHOOK_URL_SLACK_AGENT` | No | Slack webhook for **#samyak** (agent/Gemini breakdown: deadline, how to do it). |
| `SLACK_BOT_TOKEN` | No | Bot User OAuth Token (optional; for future Slack API use). |
| `WEBHOOK_URL_SLACK` | No | Fallback single Slack webhook if `WEBHOOK_URL_SLACK_TASKS` is not set. |
| `WEBHOOK_URL_DISCORD` | No | Discord webhook URL for notifications. |
| `WEBHOOK_URL_TEAMS` | No | Microsoft Teams webhook URL for notifications. |
| `SMTP_SERVER` | No | SMTP server for email (e.g. `smtp.gmail.com`). |
| `SMTP_PORT` | No | SMTP port (e.g. `587`). |
| `EMAIL_ADDRESS` | No | Sender email for reminders/summaries. |
| `EMAIL_PASSWORD` | No | SMTP password or app password. |

---

## Frontend (`.env.local`)

Copy from `env.local.example` (at repo root) to `.env.local`. Used by the Next.js dashboard.

| Variable | Required | Description |
|----------|----------|-------------|
| `NEXT_PUBLIC_API_URL` | Yes | Backend API base URL (e.g. `http://localhost:8000`). |
| `NEXT_PUBLIC_GEMINI_API_KEY` | No | Gemini API key for **frontend fallback**: when the backend is down or returns empty, the Voice Agent calls Gemini from the browser. Get key from [Google AI Studio](https://aistudio.google.com/). Restrict key for production. |
| `NEXT_PUBLIC_GEMINI_MODEL` | No | Model for frontend fallback (e.g. `gemini-2.0-flash`, `gemini-1.5-flash`). Default: `gemini-2.0-flash`. |

Firebase is **not** configured in the frontend for Firestore; all DB access is via the backend. If you use Firebase Auth in the frontend, configure that separately (e.g. in your auth provider or Firebase console).

---

## Getting credentials

1. **Gemini:** [Google AI Studio](https://aistudio.google.com/) → Get API key.
2. **Firebase:** [Firebase Console](https://console.firebase.google.com/) → Project → Project settings → Service accounts → Generate new private key. Save as JSON and set `GOOGLE_APPLICATION_CREDENTIALS` to its path.
3. **Webhooks:** Create an incoming webhook in Slack/Discord/Teams and paste the URL into the corresponding `WEBHOOK_URL_*` variable.
