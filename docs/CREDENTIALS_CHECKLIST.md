# Tools & Credentials Checklist

What you need to find or create for **Agentic Task & Management** (Remote Team Productivity).

---

## Where to paste your Gemini & Firebase values

**Do not commit real keys.** Paste them only in `backend/.env` and `.env.local` (both are gitignored).

| What you have | Where it goes | Variable name |
|---------------|---------------|---------------|
| **Gemini API key** (starts with `AIzaSy...`) | `backend/.env` | `GEMINI_API_KEY=` |
| **Firebase project ID** (e.g. `samyak-ai-7596a`) | `backend/.env` (optional) | `FIREBASE_PROJECT_ID=` |
| **Firebase Web config** (apiKey, authDomain, projectId, etc.) | `.env.local` (root) | `NEXT_PUBLIC_FIREBASE_API_KEY=`, `NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=`, `NEXT_PUBLIC_FIREBASE_PROJECT_ID=`, `NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=`, `NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=`, `NEXT_PUBLIC_FIREBASE_APP_ID=`, `NEXT_PUBLIC_FIREBASE_MEASUREMENT_ID=` |

**Backend Firestore:** The Web API key above is for the **frontend** (e.g. Firebase Auth). For the **backend** to use Firestore (tasks + working hours in the cloud), you still need a **Firebase Service Account JSON** file: Firebase Console → Project settings → Service accounts → **Generate new private key** → save the JSON, then in `backend/.env` set `USE_FIREBASE=true` and `GOOGLE_APPLICATION_CREDENTIALS=path/to/that-file.json`.

---

## Google OAuth client (Gmail, Calendar) – Agentic AI URLs

For your **Web application** OAuth client (name: samyak) used for Gmail / Calendar with the Agentic AI backend:

**First:** Remove `https://www.example.com` and any **empty** URI rows (empty = "URI must not be empty" error).

**Then use these exact values:**

### Authorised JavaScript origins (browser requests)

Add **one per line** (no trailing slash):

**Local:**
```
http://localhost:3000
http://localhost:8000
```
- `http://localhost:3000` = Next.js dashboard (frontend)
- `http://localhost:8000` = FastAPI backend (Agentic AI)

**Production (when you deploy):** add your real domains, e.g.:
```
https://your-app.vercel.app
https://api.yourdomain.com
```

### Authorised redirect URIs (where Google sends user after sign-in)

Add **one per line** (no trailing slash). Use the URL where you will handle the OAuth callback (frontend or backend).

**If your backend (FastAPI) will handle the callback** (recommended for Gmail/Calendar so the backend gets the tokens):

**Local:**
```
http://localhost:8000/api/auth/google/callback
```

**If your frontend (Next.js) will handle the callback:**
```
http://localhost:3000/auth/callback
```

**Production:** add the same path on your live domain, e.g.:
```
https://api.yourdomain.com/api/auth/google/callback
```
or
```
https://your-app.vercel.app/auth/callback
```

### Copy-paste summary (local only)

| Field | Value(s) to add |
|-------|------------------|
| **Authorised JavaScript origins** | `http://localhost:3000` and `http://localhost:8000` |
| **Authorised redirect URIs** | `http://localhost:8000/api/auth/google/callback` (backend callback) |

Save the client. You’ll get a **Client ID** and **Client secret** — put them in `backend/.env`. Example (use your real client secret from the console): `GOOGLE_OAUTH_CLIENT_ID=383813688869-0of65gai2voe3d1fgjedriajidjq5q1r.apps.googleusercontent.com`, `GOOGLE_OAUTH_CLIENT_SECRET=...`. Do not commit `.env`. Note: It can take 5 minutes to a few hours for new URIs to take effect.

---

## OAuth: Invalid Origin / Invalid Redirect (general)

If you see **"Invalid Origin"** or **"Invalid Redirect: URI must not be empty"**:

- **Do not use** `https://www.example.com`.
- **Remove** any empty URI rows.
- Use the URLs above (or your real production domains) instead.

---

## Required (must have)

### 1. Gemini API key
- **What:** Google Gemini API key (for the AI agent).
- **Where to get:** [Google AI Studio](https://aistudio.google.com/) → Get API key (or “Create API key”).
- **Where to put:** `backend/.env` → `GEMINI_API_KEY=your_key_here`
- **Note:** Without this, the Voice Agent in the dashboard won’t use live AI (you’ll see a fallback message).

### 2. Backend API URL (frontend)
- **What:** URL where your FastAPI backend runs.
- **Typical value:** `http://localhost:8000` for local dev.
- **Where to put:** `.env.local` (repo root) → `NEXT_PUBLIC_API_URL=http://localhost:8000`
- **Note:** For production, use your deployed backend URL (e.g. `https://api.yourdomain.com`).

---

## Optional but recommended

### 3. Firebase (for tasks + working hours in the cloud)
- **What:** Firebase project + **service account JSON** so the backend can use Firestore.
- **Where to get:**
  1. [Firebase Console](https://console.firebase.google.com/) → Create or select project.
  2. Project settings (gear) → **Service accounts** → **Generate new private key** → save the JSON file.
  3. Put the file somewhere safe (e.g. `backend/firebase-service-account.json`) and **do not commit it**.
- **Where to put:** `backend/.env`:
  - `USE_FIREBASE=true`
  - `GOOGLE_APPLICATION_CREDENTIALS=path/to/your-service-account.json` (path relative to `backend/` or absolute)
- **Note:** Without Firebase, tasks use a local JSON file (`data/tasks.json`) and **working hours** are not stored (log-hours feature won’t persist).

---

## Optional (nice to have)

### 4. Slack webhooks (two channels)
- **What:** Two incoming webhook URLs:
  - **#samayak-project-tasks** – when someone assigns tasks to you (task created/updated/completed).
  - **#samyak** – when the agent (Gemini) sends a detailed breakdown: deadline, how to do it, etc.
- **Where to get:** Slack app → Incoming Webhooks → Add to Slack for each channel → copy each webhook URL.
- **Where to put:** `backend/.env`:
  - `WEBHOOK_URL_SLACK_TASKS=<webhook for #samayak-project-tasks>`
  - `WEBHOOK_URL_SLACK_AGENT=<webhook for #samyak>`
- **Bot User OAuth Token (optional):** From Slack app → OAuth & Permissions → “Bot User OAuth Token”. Put in `backend/.env` as `SLACK_BOT_TOKEN=xoxb-...` if you need the Slack API later (e.g. posting as bot). Do **not** commit this.

### 5. Email (SMTP) for reminders and summaries
- **What:** SMTP server and credentials so the agent can send task reminders and productivity summaries.
- **Where to get:**
  - **Gmail:** Use an [App Password](https://support.google.com/accounts/answer/185833) (not your normal password).
  - **Other:** Use your provider’s SMTP host, port, and credentials.
- **Where to put:** `backend/.env`:
  - `SMTP_SERVER=smtp.gmail.com` (or your provider)
  - `SMTP_PORT=587`
  - `EMAIL_ADDRESS=your@email.com`
  - `EMAIL_PASSWORD=your_app_password`

### 6. Firebase Auth (if you add login with Firebase)
- **What:** Firebase Web config (apiKey, authDomain, etc.) for frontend login.
- **Where to get:** Firebase Console → Project settings → General → Your apps → Web app → config object.
- **Where to put:** In your auth setup (e.g. context or env), **not** in the Firestore backend credentials. Backend uses the **service account** (item 3); frontend Auth uses the **Web config**.

---

## Quick reference table

| Credential / tool        | Required? | Used for                    | Where to get it                    |
|--------------------------|----------|-----------------------------|------------------------------------|
| **GEMINI_API_KEY**       | Yes      | AI agent (Voice Agent)     | [Google AI Studio](https://aistudio.google.com/) |
| **NEXT_PUBLIC_API_URL**  | Yes      | Frontend → backend calls    | You set it (e.g. `http://localhost:8000`) |
| **Firebase service account** | No*  | Tasks + working hours (Firestore) | [Firebase Console](https://console.firebase.google.com/) → Service accounts |
| **WEBHOOK_URL_SLACK_TASKS** | No | Task assignments → #samayak-project-tasks | Slack Incoming Webhook for that channel |
| **WEBHOOK_URL_SLACK_AGENT** | No | Agent breakdowns → #samyak | Slack Incoming Webhook for #samyak |
| **SLACK_BOT_TOKEN**     | No       | Slack API (optional)       | Slack app OAuth & Permissions         |
| **SMTP / EMAIL_***       | No       | Email reminders & summaries| Gmail App Password or provider SMTP |
| **Firebase Auth config** | No       | Frontend login (if you use it) | Firebase Console → Web app config |

\* Required if you want working hours and cloud-backed tasks; otherwise tasks use local JSON only.

---

## Files to create from templates

1. **Backend:** `cd backend` → `cp env.example .env` → edit `.env` with the values above.
2. **Frontend:** repo root → `cp env.local.example .env.local` → set `NEXT_PUBLIC_API_URL`.

Never commit `.env` or `.env.local`; they are gitignored.
