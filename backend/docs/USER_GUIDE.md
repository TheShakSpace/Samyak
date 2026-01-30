# User Guide

Complete user guide for the Task Management & Productivity Agent.

## Getting Started

### First Time Setup

1. **Install Python 3.9+** (3.10+ recommended)
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```
4. **Run the agent:**
   ```bash
   python3 main_agent.py
   ```

## Basic Usage

### Creating Tasks

```python
from tools.task_tools import create_task

# Simple task
create_task(title="Buy groceries")

# Task with details
create_task(
    title="Finish project report",
    description="Complete quarterly report with metrics",
    priority="high",
    deadline="2 days",
    tags=["work", "urgent"]
)
```

### Viewing Tasks

```python
from tools.task_tools import get_all_tasks, get_tasks_by_priority

# Get all tasks
all_tasks = get_all_tasks()
print(f"Total tasks: {all_tasks['count']}")

# Get high priority tasks
high_priority = get_tasks_by_priority("high")
for task in high_priority['tasks']:
    print(f"- {task['title']} ({task['priority']})")
```

### Updating Tasks

```python
from tools.task_tools import update_task_status

# Mark task as in progress
update_task_status("TASK001", "in_progress")

# Complete a task
update_task_status("TASK001", "completed")
```

## Advanced Features

### Complex Queries

Use code-as-plan for complex queries:

```python
from tools.query_tools import query_tasks_with_code

# Natural language query
result = query_tasks_with_code(
    "Show me all incomplete high priority tasks due this week"
)
print(result['execution_result']['answer'])
```

### Productivity Metrics

```python
from tools.task_tools import calculate_productivity_metrics

# Get metrics for last 30 days
metrics = calculate_productivity_metrics(days=30)

print(f"Completion Rate: {metrics['completion_rate']}%")
print(f"Total Tasks: {metrics['total_tasks']}")
print(f"Completed: {metrics['status_breakdown']['completed']}")
```

### Email Notifications

```python
from tools.email_tools import send_task_reminder, send_productivity_summary

# Send reminder for tasks due tomorrow
send_task_reminder("your_email@example.com", days_ahead=1)

# Send weekly summary
send_productivity_summary("your_email@example.com", period_days=7)
```

### Visualizations

```python
from tools.visualization_tools import (
    create_productivity_chart,
    create_priority_distribution_chart
)

# Generate custom chart
result = create_productivity_chart(
    "Create a chart showing task completion rate over time",
    use_reflection=True
)

# Pre-built chart
create_priority_distribution_chart()
```

## Using the Agent

### Natural Language Interface

If you have Python 3.10+ and aisuite:

```python
from agent.orchestrator import TaskManagementAgent

agent = TaskManagementAgent()

# Natural language requests
response = agent.process_request("Show me all high priority tasks")
print(response['response'])

response = agent.process_request("Create a task to finish the report by Friday")
print(response['response'])
```

### Request Examples

- "Add a task to finish the project report by Friday with high priority"
- "Show me all incomplete tasks assigned to me"
- "What's my productivity metrics for the last week?"
- "Send me a reminder email for tasks due tomorrow"
- "Create a chart showing my task completion rate"

## Best Practices

### Task Organization

1. **Use Tags**: Organize tasks with tags
   ```python
   create_task(title="Meeting", tags=["work", "meeting", "weekly"])
   ```

2. **Set Priorities**: Use priority levels effectively
   - High: Urgent and important
   - Medium: Important but not urgent
   - Low: Nice to have

3. **Deadlines**: Set realistic deadlines
   ```python
   create_task(title="Task", deadline="1 week")  # Relative
   create_task(title="Task", deadline="2026-01-20")  # Absolute
   ```

### Productivity Tracking

1. **Regular Metrics**: Check metrics weekly
2. **Completion Tracking**: Mark tasks as completed
3. **Review Patterns**: Analyze completion rates

### Email Notifications

1. **Configure SMTP**: Set up email credentials
2. **Regular Reminders**: Schedule daily reminders
3. **Weekly Summaries**: Get productivity summaries

## Troubleshooting

### Common Issues

**Q: LLM features not working?**
A: Ensure Python 3.10+ and aisuite installed

**Q: Email not sending?**
A: Check SMTP credentials in .env file

**Q: Charts not generating?**
A: Verify matplotlib installed and data exists

**Q: Import errors?**
A: Run `pip install -r requirements.txt`

### Getting Help

1. Check the API Reference: `docs/API_REFERENCE.md`
2. Review test examples: `tests/`
3. Check development plan: `../development plan/`

## Tips and Tricks

1. **Batch Operations**: Use code-as-plan for batch updates
2. **Custom Queries**: Write custom code for specific needs
3. **Chart Reflection**: Enable reflection for better charts
4. **Email Templates**: Customize email templates if needed

---

For technical details, see API_REFERENCE.md
For deployment, see DEPLOYMENT.md

