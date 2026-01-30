# External Tools & Services Integration Guide

## Currently Supported Integrations

### ✅ OpenAI (LLM)
- **Status**: Fully integrated
- **Setup**: Add `OPENAI_API_KEY` to .env
- **Features**: Natural language, code generation, chart reflection
- **Documentation**: https://platform.openai.com/docs

### ✅ SMTP Email (Gmail, Outlook, Custom)
- **Status**: Fully integrated
- **Setup**: Add email credentials to .env
- **Features**: Reminders, summaries, notifications
- **Documentation**: See SETUP_GUIDE.md

---

## Integration Ideas (Can Be Added)

### 1. Additional LLM Providers

#### Anthropic Claude
```python
# Would require modifying:
# - tools/query_tools.py
# - utils/chart_reflection.py
# - config.py

# Add to .env:
ANTHROPIC_API_KEY=sk-ant-...
LLM_MODEL=claude-3-7-sonnet-latest
```

**Benefits**: Alternative LLM, different pricing, different capabilities

#### Google Gemini
```python
# Would require:
# - Install google-generativeai
# - Modify LLM calls
# - Update config

# Add to .env:
GOOGLE_API_KEY=...
LLM_MODEL=gemini-pro
```

---

### 2. Enhanced Email Services

#### SendGrid
```python
# Install: pip install sendgrid
# Modify: utils/email_service.py

# Add to .env:
SENDGRID_API_KEY=SG....
EMAIL_SERVICE=sendgrid
```

**Benefits**: Better deliverability, analytics, templates

#### Mailgun
```python
# Install: pip install mailgun2
# Modify: utils/email_service.py

# Add to .env:
MAILGUN_API_KEY=...
MAILGUN_DOMAIN=yourdomain.com
```

---

### 3. Database Services

#### PostgreSQL
```python
# Install: pip install psycopg2-binary sqlalchemy
# Modify: models/task.py

# Add to .env:
DATABASE_URL=postgresql://user:pass@localhost/taskdb
DB_TYPE=postgresql
```

**Benefits**: Production-ready, multi-user, better performance

#### SQLite
```python
# Install: pip install sqlalchemy
# Modify: models/task.py

# Add to .env:
DATABASE_PATH=data/tasks.db
DB_TYPE=sqlite
```

**Benefits**: No server needed, easy migration from JSON

---

### 4. Notification Services

#### Slack
```python
# Install: pip install slack-sdk
# Create: tools/slack_tools.py

# Add to .env:
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...
# Or
SLACK_BOT_TOKEN=xoxb-...
```

**Implementation**:
```python
def send_slack_notification(channel, message):
    """Send notification to Slack"""
    # Implementation here
```

#### Discord
```python
# Install: pip install discord-webhook
# Create: tools/discord_tools.py

# Add to .env:
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...
```

#### Microsoft Teams
```python
# Create: tools/teams_tools.py
# Uses webhook format

# Add to .env:
TEAMS_WEBHOOK_URL=https://outlook.office.com/webhook/...
```

---

### 5. Task Management Integrations

#### Todoist
```python
# Install: pip install todoist-api-python
# Create: tools/todoist_tools.py

# Add to .env:
TODOIST_API_KEY=...
```

**Features**:
- Sync tasks with Todoist
- Two-way sync
- Project management

#### Asana
```python
# Install: pip install asana
# Create: tools/asana_tools.py

# Add to .env:
ASANA_ACCESS_TOKEN=...
ASANA_WORKSPACE_ID=...
```

#### Trello
```python
# Install: pip install py-trello
# Create: tools/trello_tools.py

# Add to .env:
TRELLO_API_KEY=...
TRELLO_API_SECRET=...
TRELLO_TOKEN=...
```

---

### 6. Calendar Integrations

#### Google Calendar
```python
# Install: pip install google-api-python-client google-auth
# Create: tools/calendar_tools.py

# Requires OAuth setup
# Add to .env:
GOOGLE_CALENDAR_CREDENTIALS=path/to/credentials.json
```

**Features**:
- Create calendar events from tasks
- Sync deadlines
- Reminder integration

#### Outlook Calendar
```python
# Install: pip install msal
# Create: tools/outlook_tools.py

# Requires Microsoft Graph API
# Add to .env:
MICROSOFT_CLIENT_ID=...
MICROSOFT_CLIENT_SECRET=...
MICROSOFT_TENANT_ID=...
```

---

### 7. Cloud Storage

#### AWS S3
```python
# Install: pip install boto3
# Create: utils/storage.py

# Add to .env:
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_S3_BUCKET=task-agent-charts
AWS_REGION=us-east-1
```

**Features**:
- Store charts in cloud
- Backup task database
- Share charts via URLs

#### Google Cloud Storage
```python
# Install: pip install google-cloud-storage
# Create: utils/storage.py

# Add to .env:
GOOGLE_APPLICATION_CREDENTIALS=path/to/credentials.json
GCS_BUCKET_NAME=task-agent-charts
```

---

### 8. Analytics & Monitoring

#### Google Analytics
```python
# Install: pip install google-analytics-data
# Create: utils/analytics.py

# Track usage, task creation, etc.
```

#### Sentry (Error Tracking)
```python
# Install: pip install sentry-sdk
# Add to main.py:

import sentry_sdk
sentry_sdk.init("your-sentry-dsn")
```

---

## How to Add a New Integration

### Step 1: Install SDK
```bash
pip install service-sdk
```

### Step 2: Add Configuration
```python
# config.py
NEW_SERVICE_API_KEY = os.getenv("NEW_SERVICE_API_KEY")
```

### Step 3: Create Tool/Utility
```python
# tools/new_service_tools.py
def new_service_function():
    """Tool for new service"""
    # Implementation
```

### Step 4: Register Tool
```python
# agent/orchestrator.py
from tools.new_service_tools import new_service_function

self.tools.append(new_service_function)
```

### Step 5: Update Documentation
- Add to SETUP_GUIDE.md
- Update .env.example
- Document in API_REFERENCE.md

---

## Integration Priority

### High Priority (Easy to Add)
1. ✅ OpenAI - Already done
2. ✅ SMTP Email - Already done
3. 🔄 SQLite - Easy database upgrade
4. 🔄 Slack Webhooks - Simple notification

### Medium Priority (Moderate Effort)
1. 🔄 PostgreSQL - Database upgrade
2. 🔄 SendGrid - Better email service
3. 🔄 Todoist - Task sync
4. 🔄 Google Calendar - Calendar integration

### Low Priority (Complex)
1. 🔄 Multi-user support
2. 🔄 Real-time updates
3. 🔄 Web dashboard
4. 🔄 Mobile app

---

## Testing Integrations

### Test LLM Integration
```bash
python3 cli.py agent "Test request"
```

### Test Email Integration
```bash
python3 cli.py email your_email@example.com --type reminder --days 1
```

### Test New Integration
```python
# Create test script
python3 test_integration.py
```

---

## Security Considerations

### API Keys
- Store in .env (never commit)
- Use environment variables in production
- Rotate keys regularly
- Use least privilege

### OAuth (For Calendar, etc.)
- Store tokens securely
- Handle token refresh
- Implement proper scopes

### Webhooks
- Verify webhook signatures
- Use HTTPS
- Validate payloads

---

## Cost Considerations

### Free Tier Available
- ✅ OpenAI: $5 free credit
- ✅ Gmail SMTP: Free
- 🔄 SendGrid: 100 emails/day free
- 🔄 Slack: Free tier available

### Paid Services
- OpenAI: Pay-per-use (~$0.01-0.03 per request)
- SendGrid: $15/month for 40k emails
- Todoist: Free tier + paid plans
- AWS S3: Pay-per-use (very cheap)

---

## Recommended Setup for Different Use Cases

### Personal Use (Free/Minimal Cost)
```env
OPENAI_API_KEY=... (use free credits)
EMAIL_ADDRESS=... (Gmail free)
# Total: ~$0-5/month
```

### Small Team (Low Cost)
```env
OPENAI_API_KEY=... (~$10/month)
EMAIL_ADDRESS=... (Gmail free)
SLACK_WEBHOOK_URL=... (Slack free)
# Total: ~$10-20/month
```

### Production (Moderate Cost)
```env
OPENAI_API_KEY=... (~$50/month)
SENDGRID_API_KEY=... ($15/month)
POSTGRESQL_URL=... (managed DB ~$10/month)
AWS_S3_BUCKET=... (~$1/month)
# Total: ~$75-100/month
```

---

## Quick Integration Checklist

When adding a new service:

- [ ] Install SDK/package
- [ ] Add configuration to config.py
- [ ] Add environment variables to .env.example
- [ ] Create tool/utility file
- [ ] Register tool in orchestrator
- [ ] Write tests
- [ ] Update documentation
- [ ] Test integration
- [ ] Add error handling
- [ ] Update README

---

For detailed setup instructions, see `SETUP_GUIDE.md`

