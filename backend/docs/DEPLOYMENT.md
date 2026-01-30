# Deployment Guide

Guide for deploying the Task Management & Productivity Agent.

## Prerequisites

- Python 3.9+ (3.10+ recommended for full features)
- pip package manager
- OpenAI API key (for LLM features)
- Email credentials (for email notifications, optional)

## Local Deployment

### Step 1: Install Dependencies

```bash
cd task_management_agent
pip install -r requirements.txt
```

### Step 2: Configure Environment

```bash
cp .env.example .env
# Edit .env with your credentials
```

Required variables:
```env
OPENAI_API_KEY=your_key_here
LLM_MODEL=openai:gpt-4o
```

Optional variables:
```env
EMAIL_ADDRESS=your_email@example.com
EMAIL_PASSWORD=your_app_password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

### Step 3: Initialize Database

```bash
python3 main.py
```

This creates the initial task database.

### Step 4: Run the Agent

```bash
python3 main_agent.py
```

## Docker Deployment (Optional)

### Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

CMD ["python", "main_agent.py"]
```

### Build and Run

```bash
docker build -t task-agent .
docker run -d --env-file .env task-agent
```

## Production Considerations

### Security

1. **Environment Variables**: Never commit `.env` file
2. **API Keys**: Use secure secret management
3. **Email Credentials**: Use app-specific passwords
4. **Database**: Consider PostgreSQL for production

### Performance

1. **Database**: SQLite is fine for single-user, use PostgreSQL for multi-user
2. **Caching**: Consider Redis for frequently accessed data
3. **Async Operations**: Use async/await for I/O-bound operations
4. **Rate Limiting**: Implement rate limits for LLM calls

### Monitoring

1. **Logging**: Add structured logging
2. **Error Tracking**: Integrate error tracking service
3. **Metrics**: Track task creation, completion rates
4. **Health Checks**: Implement health check endpoint

### Scaling

1. **Horizontal Scaling**: Use load balancer for multiple instances
2. **Database**: Use connection pooling
3. **Task Queue**: Consider Celery for background tasks
4. **Caching**: Implement caching layer

## Cloud Deployment

### AWS

1. **EC2**: Deploy on EC2 instance
2. **Lambda**: Serverless functions for specific operations
3. **RDS**: Use RDS for PostgreSQL database
4. **S3**: Store charts and backups

### Google Cloud

1. **Compute Engine**: VM deployment
2. **Cloud Functions**: Serverless operations
3. **Cloud SQL**: Managed database
4. **Cloud Storage**: File storage

### Azure

1. **Virtual Machines**: VM deployment
2. **Functions**: Serverless functions
3. **Azure Database**: Managed database
4. **Blob Storage**: File storage

## Environment-Specific Configuration

### Development

```env
LLM_MODEL=openai:gpt-4o-mini
DEBUG=True
```

### Staging

```env
LLM_MODEL=openai:gpt-4o
DEBUG=False
```

### Production

```env
LLM_MODEL=openai:gpt-4o
DEBUG=False
LOG_LEVEL=INFO
```

## Backup and Recovery

### Database Backup

```bash
# Backup tasks
cp data/tasks.json data/backups/tasks_$(date +%Y%m%d).json
```

### Automated Backups

Set up cron job for regular backups:
```bash
0 2 * * * cp /path/to/data/tasks.json /path/to/backups/tasks_$(date +\%Y\%m\%d).json
```

## Troubleshooting

### Common Issues

1. **LLM Not Available**: Check Python version (3.10+ required)
2. **Email Not Sending**: Verify SMTP credentials
3. **Import Errors**: Ensure all dependencies installed
4. **Database Errors**: Check file permissions

### Logs

Check logs for errors:
```bash
python3 main_agent.py 2>&1 | tee agent.log
```

## Maintenance

### Regular Tasks

1. **Database Cleanup**: Archive old completed tasks
2. **Chart Cleanup**: Remove old chart files
3. **Log Rotation**: Rotate log files
4. **Dependency Updates**: Update packages regularly

### Updates

1. Pull latest changes
2. Update dependencies: `pip install -r requirements.txt --upgrade`
3. Run tests: `pytest tests/ -v`
4. Restart service

---

For more information, see the main README.md file.

