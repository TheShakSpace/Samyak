# Quick Start Guide - Running the Project

Complete guide to set up, run, and test the Task Management & Productivity Agent.

## Prerequisites

- Python 3.9+ (3.10+ recommended for full LLM features)
- pip package manager

## Step 1: Navigate to Project

```bash
cd task_management_agent
```

## Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

Or if using pip3:
```bash
pip3 install -r requirements.txt
```

## Step 3: Configure Environment (Optional)

```bash
# Copy example environment file
cp .env.example .env

# Edit .env file and add:
# OPENAI_API_KEY=your_api_key_here
# EMAIL_ADDRESS=your_email@example.com (optional)
# EMAIL_PASSWORD=your_app_password (optional)
```

**Note**: LLM features require Python 3.10+ and aisuite. Basic functionality works without it.

## Step 4: Initialize Database

```bash
python3 main.py
```

This creates the task database and sample tasks.

## Step 5: Run the Agent

### Option A: Unified Agent Interface

```bash
python3 main_agent.py
```

This shows system status and available capabilities.

### Option B: CLI Interface (Recommended)

```bash
python3 cli.py --help
```

## CLI Commands

### Check System Status

```bash
python3 cli.py status
```

### Create a Task

```bash
# Simple task
python3 cli.py create -t "Finish project report"

# Task with details
python3 cli.py create -t "Finish project report" -p high -d "2 days" --tags "work,urgent"

# Task with description
python3 cli.py create -t "Team meeting" -d "Weekly sync meeting" -p medium --deadline "1 week"
```

### List Tasks

```bash
# List all tasks
python3 cli.py list

# List high priority tasks
python3 cli.py list --priority high

# List in-progress tasks
python3 cli.py list --status in_progress

# List tasks with specific tag
python3 cli.py list --tag work

# JSON output
python3 cli.py list --json
```

### Update Task Status

```bash
# Mark as in progress
python3 cli.py update TASK001 --status in_progress

# Mark as completed
python3 cli.py update TASK001 --status completed
```

### Delete Task

```bash
python3 cli.py delete TASK001
```

### View Productivity Metrics

```bash
# Last 30 days (default)
python3 cli.py metrics

# Last 7 days
python3 cli.py metrics --days 7

# JSON output
python3 cli.py metrics --days 30 --json
```

### Generate Charts

```bash
# Priority distribution chart
python3 cli.py chart --type priority

# Completion rate chart
python3 cli.py chart --type completion --days 30

# Custom output path
python3 cli.py chart --type priority --output data/charts/my_chart.png
```

### Send Email Notifications

```bash
# Send reminder for tasks due tomorrow
python3 cli.py email your_email@example.com --type reminder --days 1

# Send weekly productivity summary
python3 cli.py email your_email@example.com --type summary --days 7
```

**Note**: Requires email configuration in .env file.

### Use Agent with Natural Language

```bash
# Requires Python 3.10+ and aisuite
python3 cli.py agent "Show me all high priority tasks"
python3 cli.py agent "Create a task to finish the report by Friday"
python3 cli.py agent "What's my productivity metrics for the last week?"
```

## Python Script Usage

### Direct Tool Usage

```python
from tools.task_tools import create_task, get_all_tasks, calculate_productivity_metrics

# Create task
result = create_task(
    title="Finish report",
    priority="high",
    deadline="2 days",
    tags=["work", "urgent"]
)
print(result['message'])

# Get all tasks
all_tasks = get_all_tasks()
print(f"Total tasks: {all_tasks['count']}")

# Get metrics
metrics = calculate_productivity_metrics(days=30)
print(f"Completion rate: {metrics['completion_rate']}%")
```

### Using the Agent

```python
from agent.orchestrator import TaskManagementAgent

# Initialize agent
agent = TaskManagementAgent()

# Process request
response = agent.process_request("Show me all high priority tasks")
print(response.get('response', response.get('message')))
```

## Testing the Project

### Run All Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov -v

# Run specific test file
pytest tests/unit/test_task_model.py -v
```

### Run Phase Tests

```bash
# Test Phase 1
python3 test_phase1.py

# Test Phase 2
python3 test_phase2.py

# Test Phase 3
python3 test_phase3.py

# Test Phase 4
python3 test_phase4.py

# Test Phase 5
python3 test_phase5.py

# Test Phase 6
python3 test_phase6.py

# Test Phase 7
python3 test_phase7.py

# Test Phase 8
python3 test_phase8.py

# Test Phase 9
python3 test_phase9.py
```

## Example Workflows

### Workflow 1: Create and Manage Tasks

```bash
# Create tasks
python3 cli.py create -t "Finish report" -p high -d "2 days"
python3 cli.py create -t "Team meeting" -p medium -d "1 week"
python3 cli.py create -t "Review code" -p low

# List all tasks
python3 cli.py list

# Update task status
python3 cli.py update TASK001 --status in_progress

# View metrics
python3 cli.py metrics
```

### Workflow 2: Query and Analyze

```bash
# List high priority tasks
python3 cli.py list --priority high

# Get productivity metrics
python3 cli.py metrics --days 30

# Generate charts
python3 cli.py chart --type priority
python3 cli.py chart --type completion --days 30
```

### Workflow 3: Email Notifications

```bash
# Check upcoming tasks
python3 cli.py list --status todo

# Send reminder
python3 cli.py email your_email@example.com --type reminder --days 1

# Send summary
python3 cli.py email your_email@example.com --type summary --days 7
```

## Troubleshooting

### Issue: Module not found

```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

### Issue: Database errors

```bash
# Check database file
ls -la data/tasks.json

# Reinitialize if needed
python3 main.py
```

### Issue: CLI not working

```bash
# Check Python version
python3 --version

# Make CLI executable
chmod +x cli.py

# Run directly
python3 cli.py --help
```

### Issue: LLM features not working

- Requires Python 3.10+
- Check: `python3 --version`
- Basic features work without LLM

### Issue: Email not sending

- Check .env file has EMAIL_ADDRESS and EMAIL_PASSWORD
- Verify SMTP credentials
- Check network connection

## Quick Reference

### Most Common Commands

```bash
# Status check
python3 cli.py status

# Create task
python3 cli.py create -t "Task title" -p high

# List tasks
python3 cli.py list

# Update task
python3 cli.py update TASK001 --status completed

# View metrics
python3 cli.py metrics

# Generate chart
python3 cli.py chart --type priority
```

### View Logs

```bash
# View latest log
tail -f logs/task_agent_*.log

# List log files
ls -lh logs/
```

### Check System Health

```bash
python3 cli.py status
```

## Next Steps

1. **Try Basic Operations**: Create, list, update tasks
2. **Explore Metrics**: Check productivity metrics
3. **Generate Charts**: Create visualizations
4. **Test Email**: Configure and send notifications
5. **Use Agent**: Try natural language requests (Python 3.10+)

## Help

For more information:
- **README.md**: Main documentation
- **docs/USER_GUIDE.md**: Detailed user guide
- **docs/API_REFERENCE.md**: Complete API reference
- **docs/DEPLOYMENT.md**: Deployment guide

---

**Ready to start?** Run: `python3 cli.py status`

