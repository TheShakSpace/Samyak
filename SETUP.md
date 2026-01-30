# Samyak AI - Setup Instructions

## Frontend Setup

### 1. Environment Variables (optional)
To point the frontend at a different backend URL, add to `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

By default the frontend uses `http://localhost:8000` for login/signup and AI (same pattern as Gemini – backend holds keys).

### 2. Install Dependencies
```bash
npm install
# or
yarn install
```

### 3. Run Development Server
```bash
npm run dev
# or
yarn dev
```

The frontend will run on http://localhost:3000

## Backend Setup

### 1. Navigate to Backend Directory
```bash
cd backend
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Create .env File
Copy `env.example` to `.env` in the backend directory and fill in your values:

```bash
cp env.example .env
```

Edit `.env` and add (same pattern as Gemini – all secrets in backend only):

```env
GEMINI_API_KEY=your_gemini_api_key_here
FIREBASE_API_KEY=your_firebase_web_api_key
FIREBASE_PROJECT_ID=your_firebase_project_id
FIREBASE_AUTH_DOMAIN=your_project_id.firebaseapp.com
FIREBASE_STORAGE_BUCKET=your_project_id.firebasestorage.app
FIREBASE_MESSAGING_SENDER_ID=your_sender_id
FIREBASE_APP_ID=your_app_id
FIREBASE_MEASUREMENT_ID=G-XXXXXXXXXX
```

Get Firebase values from Firebase Console → Project settings → General (web app config). Only `FIREBASE_API_KEY` is required for login/signup; others are optional for future use.

### 5. Run FastAPI Server
```bash
python main.py
# or
uvicorn main:app --reload
```

The backend will run on http://localhost:8000

## Firebase Setup (backend only)

1. Go to https://console.firebase.google.com
2. Create or use a project (e.g. "samyak-ai")
3. Enable Authentication → Sign-in method → Email/Password
4. In Project settings → General, copy the web app config (apiKey, projectId, etc.) into `backend/.env` as in step 4 above. No Firebase config on the frontend – login/signup go through the backend (same pattern as Gemini).

## Authentication Flow

1. Users sign up at `/auth/signup` with name, email, and password
2. Frontend calls backend `POST /api/auth/signup`; backend uses Firebase REST API to create the user
3. Users login at `/auth/login`; frontend calls backend `POST /api/auth/login`
4. Backend returns token and user; frontend stores them and redirects to `/dashboard`
5. Dashboard displays the AI agent room with voice capabilities

## AI Integration

### Gemini API
- Used for intelligent chat responses
- Handles document analysis
- Generates strategic recommendations
- Backend routes: `/api/chat`, `/api/analyze`, `/api/generate-strategy`

## Project Structure

```
├── app/
│   ├── auth/
│   │   ├── login/
│   │   └── signup/
│   ├── dashboard/
│   └── page.tsx
├── lib/
│   ├── api.ts
│   ├── gemini.ts
│   └── ai-service.ts
├── context/
│   └── auth-context.tsx
├── components/
│   ├── agent-room.tsx
│   └── ...
└── backend/
    ├── main.py
    └── requirements.txt
```

## Next Steps

1. Copy `backend/env.example` to `backend/.env` and add your Gemini and Firebase keys (Firebase API key from Project settings → General).
2. Start the backend: `cd backend && pip install -r requirements.txt && python main.py`
3. Start the frontend: `npm run dev`
4. Visit http://localhost:3000
5. Sign up and test the dashboard (login/signup go through the backend; no Firebase on frontend)
