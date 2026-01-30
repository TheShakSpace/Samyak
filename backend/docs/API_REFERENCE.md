# API Reference

Complete API documentation for the Task Management & Productivity Agent.

## Task Management Tools

### create_task

Create a new task and add it to the task database.

**Signature:**
```python
create_task(
    title: str,
    description: str = "",
    priority: str = "medium",
    deadline: Optional[str] = None,
    assignee: str = "me",
    tags: Optional[List[str]] = None,
) -> Dict
```

**Parameters:**
- `title` (str, required): Task title
- `description` (str): Detailed description
- `priority` (str): "high", "medium", or "low" (default: "medium")
- `deadline` (str, optional): ISO date or relative ("2 days", "1 week")
- `assignee` (str): Person assigned (default: "me")
- `tags` (List[str]): Categorization tags

**Returns:**
```python
{
    "task_id": str,
    "status": "success",
    "message": str,
    "task": dict
}
```

**Example:**
```python
result = create_task(
    title="Finish report",
    priority="high",
    deadline="2 days",
    tags=["work", "urgent"]
)
```

---

### update_task_status

Update the status of a task.

**Signature:**
```python
update_task_status(task_id: str, status: str) -> Dict
```

**Parameters:**
- `task_id` (str): Task identifier
- `status` (str): "todo", "in_progress", or "completed"

**Returns:**
```python
{
    "status": "success" | "error",
    "message": str,
    "task": dict | None
}
```

---

### get_tasks_by_priority

Get tasks filtered by priority level.

**Signature:**
```python
get_tasks_by_priority(priority: Optional[str] = None) -> Dict
```

**Parameters:**
- `priority` (str, optional): "high", "medium", "low", or None for all

**Returns:**
```python
{
    "count": int,
    "priority": str,
    "tasks": List[dict]
}
```

---

### get_all_tasks

Get all tasks with optional filtering.

**Signature:**
```python
get_all_tasks(
    status: Optional[str] = None,
    assignee: Optional[str] = None,
    tag: Optional[str] = None,
) -> Dict
```

**Parameters:**
- `status` (str, optional): Filter by status
- `assignee` (str, optional): Filter by assignee
- `tag` (str, optional): Filter by tag

**Returns:**
```python
{
    "count": int,
    "filters": dict,
    "tasks": List[dict]
}
```

---

### calculate_productivity_metrics

Calculate productivity metrics.

**Signature:**
```python
calculate_productivity_metrics(
    assignee: Optional[str] = None,
    days: int = 30
) -> Dict
```

**Returns:**
```python
{
    "period_days": int,
    "assignee": str,
    "total_tasks": int,
    "status_breakdown": dict,
    "priority_breakdown": dict,
    "completion_rate": float,
    "average_completion_hours": float | None
}
```

---

## Query Tools

### query_tasks_with_code

Query tasks using code-as-plan pattern.

**Signature:**
```python
query_tasks_with_code(
    user_request: str,
    model: str = LLM_MODEL
) -> Dict
```

**Example:**
```python
result = query_tasks_with_code(
    "Show me all incomplete high priority tasks due this week"
)
```

---

## Email Tools

### send_task_reminder

Send reminder email for tasks due soon.

**Signature:**
```python
send_task_reminder(
    to_address: str,
    days_ahead: int = 1,
    assignee: Optional[str] = None
) -> Dict
```

---

### send_productivity_summary

Send productivity summary email.

**Signature:**
```python
send_productivity_summary(
    to_address: str,
    period_days: int = 7,
    assignee: Optional[str] = None
) -> Dict
```

---

## Visualization Tools

### create_productivity_chart

Create productivity chart with optional reflection.

**Signature:**
```python
create_productivity_chart(
    instruction: str,
    output_path: Optional[str] = None,
    model: str = "openai:gpt-4o",
    use_reflection: bool = True
) -> Dict
```

**Example:**
```python
result = create_productivity_chart(
    "Create a bar chart showing task count by priority",
    use_reflection=True
)
```

---

## Agent API

### TaskManagementAgent

Main agent orchestrator.

**Methods:**
- `process_request(request: str, use_llm: bool = True) -> Dict`
- `get_available_tools() -> List[Dict]`
- `get_system_status() -> Dict`

**Example:**
```python
from agent.orchestrator import TaskManagementAgent

agent = TaskManagementAgent()
response = agent.process_request("Show me all high priority tasks")
```

---

## Data Models

### Task

Task data model.

**Attributes:**
- `task_id`: str
- `title`: str
- `description`: str
- `priority`: str ("high", "medium", "low")
- `deadline`: datetime | None
- `status`: str ("todo", "in_progress", "completed")
- `assignee`: str
- `tags`: List[str]
- `created_at`: datetime
- `updated_at`: datetime
- `completed_at`: datetime | None

**Methods:**
- `to_dict() -> dict`: Serialize to dictionary
- `from_dict(data: dict) -> Task`: Deserialize from dictionary

---

## Error Handling

All tools return dictionaries with a `status` field:
- `"success"`: Operation completed successfully
- `"error"`: Operation failed (check `message` field)
- `"info"`: Informational message

Always check the `status` field before using results.

