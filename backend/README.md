# Task Management & Productivity Agent

A comprehensive task management agent that combines **all four agentic AI patterns**:
1. **Tool Calling** - Task CRUD operations and priority calculations
2. **Email Assistant Workflow** - Automated reminders and notifications
3. **Code-as-Plan** - Dynamic query generation for task analytics
4. **Chart Generation with Reflection** - Productivity visualizations with iterative improvement

## Features

### Task Management
- Create, read, update, delete tasks
- Priority calculation and tracking
- Status management (todo, in_progress, completed)
- Tag-based organization
- Deadline management with flexible date parsing

### Dynamic Queries
- Natural language query processing
- Code generation for complex filters
- Safe code execution environment
- Flexible filtering (priority, status, dates, tags, assignee)

### Email Notifications
- Task reminders (configurable days ahead)
- Productivity summaries (daily/weekly)
- Task completion notifications
- Custom email support

### Visualizations
- Chart generation from natural language
- Reflection mechanism for chart improvement
- Pre-built charts (completion rate, priority distribution)
- Multiple chart types supported

### Intelligent Agent
- Request routing and categorization
- Tool recommendation system
- Unified interface for all operations
- System status monitoring

## Quick Start

### Installation

1. **Clone or navigate to the project:**
```bash
cd task_management_agent
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables:**
```bash
cp .env.example .env
# Edit .env and add your API keys and email credentials
```

4. **Run the agent:**
```bash
python3 main_agent.py
```

### Basic Usage

#### Direct Tool Usage

```python
from tools.task_tools import create_task, get_all_tasks, calculate_productivity_metrics

# Create a task
result = create_task(
    title="Finish project report",
    priority="high",
    deadline="2 days",
    tags=["work", "urgent"]
)

# Get all tasks
all_tasks = get_all_tasks()

# Calculate productivity metrics
metrics = calculate_productivity_metrics(days=30)
print(f"Completion rate: {metrics['completion_rate']}%")
```

#### Using the Agent (requires Python 3.10+)

```python
from agent.orchestrator import TaskManagementAgent

# Initialize agent
agent = TaskManagementAgent()

# Process natural language request
response = agent.process_request("Show me all high priority tasks")
print(response['response'])
```

## Project Structure

```
task_management_agent/
├── main.py                    # Phase 1 entry point
├── main_agent.py             # Phase 6 unified agent
├── config.py                  # Configuration
├── requirements.txt           # Dependencies
├── pytest.ini                 # Test configuration
├── models/
│   └── task.py               # Task model & TaskManager
├── tools/
│   ├── task_tools.py         # Task management tools (6 tools)
│   ├── query_tools.py        # Code-as-plan tools
│   ├── email_tools.py        # Email tools (5 tools)
│   └── visualization_tools.py # Chart tools (5 tools)
├── agent/
│   ├── orchestrator.py       # Main agent controller
│   └── router.py             # Request routing
├── utils/
│   ├── code_executor.py      # Safe code execution
│   ├── email_service.py      # Email service
│   └── chart_reflection.py   # Chart reflection
├── templates/
│   └── email_templates.py     # Email templates
├── data/
│   ├── tasks.json            # Task database
│   └── charts/               # Generated charts
└── tests/
    ├── unit/                 # Unit tests
    ├── integration/          # Integration tests
    └── conftest.py           # Test fixtures
```

## Configuration

### Environment Variables (.env)

```env
# LLM Configuration
OPENAI_API_KEY=your_api_key_here
LLM_MODEL=openai:gpt-4o

# Email Configuration (optional)
EMAIL_ADDRESS=your_email@example.com
EMAIL_PASSWORD=your_app_password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

### Dependencies

```
aisuite>=0.1.0          # LLM client (requires Python 3.10+)
pandas>=1.0.0           # Data manipulation
matplotlib>=3.0.0       # Chart generation
python-dotenv>=0.19.0   # Environment variables
python-dateutil>=2.8.0  # Date parsing
pytest>=7.0.0           # Testing (optional)
pytest-cov>=4.0.0       # Coverage (optional)
```

## Usage Examples

### Task Management

```python
from tools.task_tools import (
    create_task,
    update_task_status,
    get_tasks_by_priority,
    get_all_tasks
)

# Create task with relative deadline
create_task(
    title="Team meeting",
    description="Weekly sync meeting",
    priority="high",
    deadline="1 week",
    tags=["meeting", "weekly"]
)

# Update task status
update_task_status("TASK001", "in_progress")

# Get high priority tasks
high_priority = get_tasks_by_priority("high")

# Filter tasks
tasks = get_all_tasks(status="in_progress", tag="work")
```

### Code-as-Plan Queries

```python
from tools.query_tools import query_tasks_with_code

# Complex query
result = query_tasks_with_code(
    "Show me all incomplete high priority tasks due this week"
)
print(result['execution_result']['answer'])
```

### Email Notifications

```python
from tools.email_tools import (
    send_task_reminder,
    send_productivity_summary
)

# Send reminder for tasks due tomorrow
send_task_reminder("user@example.com", days_ahead=1)

# Send weekly productivity summary
send_productivity_summary("user@example.com", period_days=7)
```

### Visualizations

```python
from tools.visualization_tools import (
    create_productivity_chart,
    create_priority_distribution_chart,
    create_task_completion_chart
)

# Generate chart with reflection
result = create_productivity_chart(
    "Create a chart showing task completion rate over time",
    use_reflection=True
)

# Pre-built charts
create_priority_distribution_chart()
create_task_completion_chart(days=30)
```

## Testing

### Run All Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov -v

# Run specific category
pytest tests/unit/ -v
pytest tests/integration/ -v
```

### Test Coverage

The project includes comprehensive tests:
- **Unit Tests**: Task model, TaskManager, tool functions
- **Integration Tests**: End-to-end workflows, error handling
- **Test Fixtures**: Isolated testing with temporary databases

## Development Phases

The project was built in 7 phases:

1. **Phase 1**: Setup & Task Data Structure ✅
2. **Phase 2**: Build Task Management Tools ✅
3. **Phase 3**: Code-as-Plan for Task Queries ✅
4. **Phase 4**: Email Integration ✅
5. **Phase 5**: Visualization with Reflection ✅
6. **Phase 6**: Integration & Orchestration ✅
7. **Phase 7**: Testing & Quality Assurance ✅

## API Reference

### Task Tools

- `create_task(title, description, priority, deadline, assignee, tags)` - Create new task
- `update_task_status(task_id, status)` - Update task status
- `get_tasks_by_priority(priority)` - Filter by priority
- `get_all_tasks(status, assignee, tag)` - Get tasks with filters
- `calculate_productivity_metrics(assignee, days)` - Calculate metrics
- `delete_task(task_id)` - Delete task

### Query Tools

- `query_tasks_with_code(user_request, model)` - Code-as-plan query
- `generate_query_code(user_request, model)` - Generate query code
- `execute_query_code(code, user_request)` - Execute query code

### Email Tools

- `send_task_reminder(to_address, days_ahead, assignee)` - Send reminders
- `send_productivity_summary(to_address, period_days, assignee)` - Send summary
- `send_task_completion_notification(to_address, task_id)` - Completion notification
- `send_custom_email(to_address, subject, body)` - Custom email
- `get_upcoming_tasks_for_reminder(days_ahead, assignee)` - Get upcoming tasks

### Visualization Tools

- `create_productivity_chart(instruction, output_path, model, use_reflection)` - Generate chart
- `create_task_completion_chart(days, output_path)` - Completion rate chart
- `create_priority_distribution_chart(output_path)` - Priority distribution chart
- `generate_chart_code(instruction, output_path, model)` - Generate chart code
- `execute_chart_code(code, tasks)` - Execute chart code

## Requirements

- **Python**: 3.9+ (3.10+ recommended for full LLM features)
- **OpenAI API Key**: For LLM features (optional for basic functionality)
- **Email Credentials**: For email notifications (optional)

## Limitations

- **LLM Features**: Require Python 3.10+ and aisuite
- **Email Sending**: Requires valid SMTP credentials
- **Chart Reflection**: Requires Python 3.10+ and vision-capable LLM

## Contributing

1. Run tests before submitting changes
2. Follow existing code style
3. Add tests for new features
4. Update documentation

## License

This project is part of an educational course on Agentic AI.

## Support

For issues or questions, refer to the development plan documentation in `../development plan/`.

---

**Status**: ✅ Production Ready
**Version**: 1.0.0
**Last Updated**: January 2026
