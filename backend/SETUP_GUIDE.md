# Complete Setup Guide - Environment & External Tools

## Overview

This guide covers setting up environment variables and connecting external tools/services to enhance the Task Management Agent.

---

## Step 1: Create .env File

```bash
cd task_management_agent
cp .env.example .env
# Or create manually:
touch .env
```

---

## Step 2: Required vs Optional Configuration

### ✅ Required (Core Functionality Works Without These)
- None! Core features work without any configuration.

### ⚠️ Optional (Enables Additional Features)

1. **LLM Configuration** - Enables natural language agent features
2. **Email Configuration** - Enables email notifications
3. **Custom Settings** - Database paths, chart directories, etc.

---

## Environment Variables Setup

### LLM Configuration (Optional - Requires Python 3.10+)

**Purpose**: Enables natural language processing, code generation, and chart reflection

#### Option 1: OpenAI (Recommended)

```env
# OpenAI Configuration
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
LLM_MODEL=openai:gpt-4o
```

**How to Get OpenAI API Key**:
1. Go to https://platform.openai.com/
2. Sign up or log in
3. Navigate to API Keys section
4. Click "Create new secret key"
5. Copy the key (starts with `sk-proj-` or `sk-`)

**Available Models**:
- `openai:gpt-4o` - Best for complex tasks (recommended)
- `openai:gpt-4o-mini` - Faster, cheaper, good for simple tasks
- `openai:gpt-4.1` - Strong reasoning
- `openai:gpt-4.1-mini` - Lighter version

#### Option 2: Anthropic Claude (Alternative)

```env
# Anthropic Configuration
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
LLM_MODEL=claude-3-7-sonnet-latest
```

**How to Get Anthropic API Key**:
1. Go to https://console.anthropic.com/
2. Sign up or log in
3. Navigate to API Keys
4. Create new key
5. Copy the key

**Note**: You'll need to modify the code to use Anthropic client instead of OpenAI.

---

### Email Configuration (Optional)

**Purpose**: Enables email notifications, reminders, and productivity summaries

#### Gmail Setup (Recommended)

```env
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

**How to Get Gmail App Password**:
1. Go to https://myaccount.google.com/
2. Enable 2-Step Verification (if not already)
3. Go to App Passwords: https://myaccount.google.com/apppasswords
4. Select "Mail" and "Other (Custom name)"
5. Enter "Task Agent" as name
6. Click "Generate"
7. Copy the 16-character password (use this, NOT your regular password)

#### Outlook/Hotmail Setup

```env
EMAIL_ADDRESS=your_email@outlook.com
EMAIL_PASSWORD=your_password
SMTP_SERVER=smtp-mail.outlook.com
SMTP_PORT=587
```

#### Custom SMTP Server

```env
EMAIL_ADDRESS=your_email@yourdomain.com
EMAIL_PASSWORD=your_password
SMTP_SERVER=smtp.yourdomain.com
SMTP_PORT=587
# Or 465 for SSL
```

**Common SMTP Settings**:
- **Gmail**: smtp.gmail.com:587
- **Outlook**: smtp-mail.outlook.com:587
- **Yahoo**: smtp.mail.yahoo.com:587
- **Custom**: Check with your email provider

---

### Advanced Configuration (Optional)

```env
# Database Path (default: data/tasks.json)
TASKS_DB_PATH=data/tasks.json

# Chart Output Directory (default: data/charts)
CHART_OUTPUT_DIR=data/charts

# Log Level (default: INFO)
LOG_LEVEL=INFO
# Options: DEBUG, INFO, WARNING, ERROR

# Custom LLM Model
LLM_MODEL=openai:gpt-4o-mini
```

---

## Complete .env File Example

```env
# ============================================
# LLM Configuration (Optional - Python 3.10+)
# ============================================
OPENAI_API_KEY=sk-proj-your-key-here
LLM_MODEL=openai:gpt-4o

# ============================================
# Email Configuration (Optional)
# ============================================
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password_here
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

# ============================================
# Advanced Settings (Optional)
# ============================================
TASKS_DB_PATH=data/tasks.json
CHART_OUTPUT_DIR=data/charts
LOG_LEVEL=INFO
```

---

## External Tools & Services You Can Connect

### 1. LLM Services (For Agent Features)

#### ✅ OpenAI (Currently Supported)
- **Service**: OpenAI API
- **Features**: Natural language processing, code generation, chart reflection
- **Setup**: Add `OPENAI_API_KEY` to .env
- **Cost**: Pay-per-use (check pricing at platform.openai.com)
- **Status**: ✅ Ready to use

#### 🔄 Anthropic Claude (Can Be Added)
- **Service**: Anthropic API
- **Features**: Alternative LLM provider
- **Setup**: Requires code modification
- **Cost**: Pay-per-use
- **Status**: ⚠️ Requires code changes

#### 🔄 Google Gemini (Can Be Added)
- **Service**: Google AI Studio
- **Features**: Another LLM option
- **Setup**: Requires code modification
- **Cost**: Pay-per-use
- **Status**: ⚠️ Requires code changes

**How to Add New LLM Provider**:
1. Install provider SDK
2. Modify `tools/query_tools.py` and `utils/chart_reflection.py`
3. Update `config.py` to support new provider
4. Test integration

---

### 2. Email Services (For Notifications)

#### ✅ Gmail (Currently Supported)
- **Service**: Gmail SMTP
- **Features**: Send reminders, summaries, notifications
- **Setup**: Add Gmail credentials to .env
- **Status**: ✅ Ready to use

#### ✅ Outlook/Hotmail (Currently Supported)
- **Service**: Outlook SMTP
- **Features**: Email notifications
- **Setup**: Add Outlook credentials to .env
- **Status**: ✅ Ready to use

#### ✅ Custom SMTP (Currently Supported)
- **Service**: Any SMTP server
- **Features**: Email notifications
- **Setup**: Add SMTP settings to .env
- **Status**: ✅ Ready to use

#### 🔄 SendGrid (Can Be Added)
- **Service**: SendGrid API
- **Features**: Transactional emails, better deliverability
- **Setup**: Requires code modification
- **Status**: ⚠️ Requires code changes

#### 🔄 Mailgun (Can Be Added)
- **Service**: Mailgun API
- **Features**: Email API service
- **Setup**: Requires code modification
- **Status**: ⚠️ Requires code changes

**How to Add Email Service**:
1. Install service SDK (e.g., `sendgrid`, `mailgun`)
2. Modify `utils/email_service.py`
3. Add service-specific configuration
4. Update email tools

---

### 3. Database Services (Can Be Added)

#### 🔄 PostgreSQL (Can Be Added)
- **Service**: PostgreSQL database
- **Features**: Better for production, multi-user support
- **Setup**: Requires code modification
- **Status**: ⚠️ Architecture ready, needs implementation

**How to Add PostgreSQL**:
1. Install `psycopg2` or `sqlalchemy`
2. Modify `models/task.py` TaskManager
3. Update database connection logic
4. Migrate from JSON to PostgreSQL

#### 🔄 SQLite (Can Be Added)
- **Service**: SQLite database
- **Features**: Local database, no server needed
- **Setup**: Requires code modification
- **Status**: ⚠️ Easy to add

#### 🔄 MongoDB (Can Be Added)
- **Service**: MongoDB
- **Features**: Document database
- **Setup**: Requires code modification
- **Status**: ⚠️ Requires code changes

---

### 4. Cloud Storage (Can Be Added)

#### 🔄 AWS S3 (Can Be Added)
- **Service**: Amazon S3
- **Features**: Store charts, backups
- **Setup**: Requires `boto3` and AWS credentials
- **Status**: ⚠️ Requires code changes

#### 🔄 Google Cloud Storage (Can Be Added)
- **Service**: GCS
- **Features**: Store charts, backups
- **Setup**: Requires GCS SDK
- **Status**: ⚠️ Requires code changes

---

### 5. Task Management Integrations (Can Be Added)

#### 🔄 Todoist API (Can Be Added)
- **Service**: Todoist
- **Features**: Sync with Todoist
- **Setup**: Requires Todoist API key
- **Status**: ⚠️ Requires code changes

#### 🔄 Asana API (Can Be Added)
- **Service**: Asana
- **Features**: Sync with Asana projects
- **Setup**: Requires Asana API
- **Status**: ⚠️ Requires code changes

#### 🔄 Trello API (Can Be Added)
- **Service**: Trello
- **Features**: Sync with Trello boards
- **Setup**: Requires Trello API
- **Status**: ⚠️ Requires code changes

---

### 6. Notification Services (Can Be Added)

#### 🔄 Slack (Can Be Added)
- **Service**: Slack Webhooks/API
- **Features**: Send notifications to Slack
- **Setup**: Requires Slack webhook URL
- **Status**: ⚠️ Requires code changes

#### 🔄 Discord (Can Be Added)
- **Service**: Discord Webhooks
- **Features**: Send notifications to Discord
- **Setup**: Requires Discord webhook
- **Status**: ⚠️ Requires code changes

#### 🔄 Microsoft Teams (Can Be Added)
- **Service**: Teams Webhooks
- **Features**: Send notifications to Teams
- **Setup**: Requires Teams webhook
- **Status**: ⚠️ Requires code changes

---

### 7. Calendar Integrations (Can Be Added)

#### 🔄 Google Calendar (Can Be Added)
- **Service**: Google Calendar API
- **Features**: Sync tasks with calendar
- **Setup**: Requires OAuth and Calendar API
- **Status**: ⚠️ Requires code changes

#### 🔄 Outlook Calendar (Can Be Added)
- **Service**: Microsoft Graph API
- **Features**: Sync with Outlook calendar
- **Setup**: Requires Microsoft API
- **Status**: ⚠️ Requires code changes

---

## Step-by-Step Setup Instructions

### Minimal Setup (Core Features Only)

```bash
# 1. Navigate to project
cd task_management_agent

# 2. Install dependencies (without aisuite)
pip3 install -r requirements.txt

# 3. No .env file needed!
# Core features work without configuration

# 4. Run the project
python3 cli.py status
```

**What Works**: Task management, charts, metrics, CLI - everything except LLM features

---

### Full Setup (With LLM Features)

```bash
# 1. Ensure Python 3.10+
python3 --version  # Should be 3.10 or higher

# 2. Create .env file
cat > .env << EOF
OPENAI_API_KEY=sk-proj-your-key-here
LLM_MODEL=openai:gpt-4o
EOF

# 3. Install full dependencies
pip3 install -r requirements-full.txt

# 4. Verify
python3 cli.py status
# Should show: LLM: ✓
```

---

### Email Setup

```bash
# 1. Get email app password (see Gmail setup above)

# 2. Add to .env
cat >> .env << EOF
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EOF

# 3. Test email
python3 cli.py email your_email@gmail.com --type reminder --days 1
```

---

## Verification Steps

### Check Configuration

```bash
# Check what's configured
python3 cli.py status
```

**Expected Output**:
```
System Status:
  Health: HEALTHY
  
  Configuration:
    Database: ✓
    LLM: ✓ (if configured)
    Email: ✓ (if configured)
```

### Test LLM (If Configured)

```bash
# Test natural language
python3 cli.py agent "Show me all high priority tasks"
```

### Test Email (If Configured)

```bash
# Test email sending
python3 cli.py email your_email@example.com --type reminder --days 1
```

---

## Troubleshooting

### Issue: LLM Not Working

**Symptoms**: `LLM: ✗` in status

**Solutions**:
1. Check Python version: `python3 --version` (needs 3.10+)
2. Check API key in .env
3. Verify key is valid (test at platform.openai.com)
4. Check internet connection

### Issue: Email Not Sending

**Symptoms**: Email sent: False

**Solutions**:
1. Verify email credentials in .env
2. For Gmail: Use App Password, not regular password
3. Check SMTP server and port
4. Verify network/firewall allows SMTP
5. Test SMTP connection manually

### Issue: Module Not Found

**Solutions**:
```bash
# Reinstall dependencies
pip3 install -r requirements.txt --upgrade

# Or for full features
pip3 install -r requirements-full.txt --upgrade
```

---

## Security Best Practices

### 1. Never Commit .env File

```bash
# Ensure .env is in .gitignore
echo ".env" >> .gitignore
```

### 2. Use App Passwords

- Never use your main email password
- Always use app-specific passwords
- Rotate passwords regularly

### 3. Protect API Keys

- Don't share .env file
- Don't commit keys to git
- Use environment variables in production
- Consider secret management services

### 4. Limit API Access

- Use API key restrictions when possible
- Monitor API usage
- Set usage limits

---

## Production Deployment

### Environment Variables in Production

**Option 1: Environment Variables**
```bash
export OPENAI_API_KEY=your_key
export EMAIL_ADDRESS=your_email
# etc.
```

**Option 2: Secret Management**
- AWS Secrets Manager
- Google Secret Manager
- Azure Key Vault
- HashiCorp Vault

**Option 3: Docker Secrets**
```yaml
# docker-compose.yml
secrets:
  openai_key:
    external: true
```

---

## Integration Roadmap

### Easy to Add (Low Effort)

1. **SQLite Database** - Replace JSON with SQLite
2. **Slack Notifications** - Add webhook support
3. **Discord Notifications** - Add webhook support
4. **Additional LLM Providers** - Add Anthropic, Gemini

### Medium Effort

1. **PostgreSQL** - Database migration
2. **SendGrid** - Email service integration
3. **Todoist Sync** - API integration
4. **Google Calendar** - Calendar sync

### Advanced (Higher Effort)

1. **Multi-user Support** - User authentication
2. **Real-time Updates** - WebSocket support
3. **Mobile App** - API backend
4. **Web Dashboard** - Frontend interface

---

## Quick Reference

### Minimal .env (Core Features)
```env
# Empty - everything works!
```

### Basic .env (With LLM)
```env
OPENAI_API_KEY=sk-proj-your-key
LLM_MODEL=openai:gpt-4o
```

### Full .env (All Features)
```env
OPENAI_API_KEY=sk-proj-your-key
LLM_MODEL=openai:gpt-4o
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

---

## Next Steps

1. **Start Minimal**: Use without .env to test core features
2. **Add LLM**: Get OpenAI key for agent features
3. **Add Email**: Configure email for notifications
4. **Extend**: Add custom integrations as needed

---

**Remember**: The project works perfectly without any configuration! All core features are available. LLM and email are optional enhancements.

