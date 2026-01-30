import os
from pathlib import Path
from dotenv import load_dotenv

# Load from backend/.env when running from backend dir
_env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(_env_path)
load_dotenv()

TASKS_DB_PATH = "data/tasks.json"
CHART_OUTPUT_DIR = "data/charts"

# --- LLM: Gemini (default) ---
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = (os.getenv("GEMINI_MODEL", "gemini-2.0-flash") or "").strip() or "gemini-2.0-flash"

# Legacy (fallback only)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", None)
LLM_MODEL = os.getenv("LLM_MODEL", "openai:gpt-4o")
LLAMA_MODEL_PATH = os.getenv("LLAMA_MODEL_PATH", None)
LLAMA_N_CTX = int(os.getenv("LLAMA_N_CTX", "4096"))
LLAMA_N_THREADS = int(os.getenv("LLAMA_N_THREADS", "4"))
LLAMA_MODEL_NAME = os.getenv("LLAMA_MODEL_NAME", "llama-3.3-70b-instruct")

# --- Firebase (backend only) ---
USE_FIREBASE = os.getenv("USE_FIREBASE", "false").lower() in ("true", "1", "yes")
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "")
FIREBASE_PROJECT_ID = os.getenv("FIREBASE_PROJECT_ID", "")

# --- Google OAuth (Gmail, Calendar) ---
GOOGLE_OAUTH_CLIENT_ID = os.getenv("GOOGLE_OAUTH_CLIENT_ID", "")
GOOGLE_OAUTH_CLIENT_SECRET = os.getenv("GOOGLE_OAUTH_CLIENT_SECRET", "")

# --- Backend & webhooks ---
BACKEND_BASE_URL = os.getenv("BACKEND_BASE_URL", "http://localhost:8000")
# Slack: two webhooks – tasks channel (assignments), agent channel (Gemini breakdowns)
WEBHOOK_URL_SLACK_TASKS = os.getenv("WEBHOOK_URL_SLACK_TASKS", "")   # e.g. #samayak-project-tasks
WEBHOOK_URL_SLACK_AGENT = os.getenv("WEBHOOK_URL_SLACK_AGENT", "")    # e.g. #samyak (agent breakdowns)
WEBHOOK_URL_SLACK = os.getenv("WEBHOOK_URL_SLACK", "")               # fallback single webhook
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN", "")                   # Bot User OAuth Token (optional, for future API use)
WEBHOOK_URL_DISCORD = os.getenv("WEBHOOK_URL_DISCORD", "")
WEBHOOK_URL_TEAMS = os.getenv("WEBHOOK_URL_TEAMS", "")

EMAIL_CONFIG = {
    "smtp_server": os.getenv("SMTP_SERVER", "smtp.gmail.com"),
    "smtp_port": int(os.getenv("SMTP_PORT", "587")),
    "email_address": os.getenv("EMAIL_ADDRESS", ""),
    "email_password": os.getenv("EMAIL_PASSWORD", ""),
}

