from datetime import datetime, timedelta
from typing import Optional, List, Dict
from models.task import Task
from db.factory import get_task_manager_factory

task_manager = get_task_manager_factory()


def create_task(
    title: str,
    description: str = "",
    priority: str = "medium",
    deadline: Optional[str] = None,
    assignee: str = "me",
    tags: Optional[List[str]] = None,
) -> Dict:
    """
    Create a new task and add it to the task database.
    
    Args:
        title: The title of the task (required)
        description: Detailed description of the task
        priority: Task priority - "high", "medium", or "low" (default: "medium")
        deadline: Deadline in ISO format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS) or relative like "2 days", "1 week"
        assignee: Person assigned to the task (default: "me")
        tags: List of tags for categorization
    
    Returns:
        Dictionary with task_id and confirmation message
    """
    import uuid
    from dateutil import parser
    
    task_id = f"TASK{uuid.uuid4().hex[:6].upper()}"
    
    deadline_dt = None
    if deadline:
        try:
            if any(keyword in deadline.lower() for keyword in ["day", "week", "month", "hour"]):
                now = datetime.now()
                if "day" in deadline.lower():
                    days = int(''.join(filter(str.isdigit, deadline)) or "0")
                    deadline_dt = now + timedelta(days=days)
                elif "week" in deadline.lower():
                    weeks = int(''.join(filter(str.isdigit, deadline)) or "0")
                    deadline_dt = now + timedelta(weeks=weeks)
                elif "month" in deadline.lower():
                    months = int(''.join(filter(str.isdigit, deadline)) or "0")
                    deadline_dt = now + timedelta(days=months * 30)
            else:
                deadline_dt = parser.parse(deadline)
        except:
            deadline_dt = None
    
    task = Task(
        task_id=task_id,
        title=title,
        description=description,
        priority=priority.lower(),
        deadline=deadline_dt,
        status="todo",
        assignee=assignee,
        tags=tags or [],
    )
    
    task_manager.add_task(task)
    
    return {
        "task_id": task_id,
        "status": "success",
        "message": f"Task '{title}' created successfully with ID {task_id}",
        "task": task.to_dict(),
    }


def update_task_status(task_id: str, status: str) -> Dict:
    """
    Update the status of a task.
    
    Args:
        task_id: The unique identifier of the task
        status: New status - "todo", "in_progress", or "completed"
    
    Returns:
        Dictionary with update confirmation
    """
    valid_statuses = ["todo", "in_progress", "completed"]
    status = status.lower()
    
    if status not in valid_statuses:
        return {
            "status": "error",
            "message": f"Invalid status. Must be one of: {', '.join(valid_statuses)}",
        }
    
    task = task_manager.get_task(task_id)
    if not task:
        return {
            "status": "error",
            "message": f"Task with ID {task_id} not found",
        }
    
    update_data = {"status": status}
    if status == "completed":
        update_data["completed_at"] = datetime.now()
    
    updated_task = task_manager.update_task(task_id, **update_data)
    
    return {
        "status": "success",
        "message": f"Task {task_id} status updated to '{status}'",
        "task": updated_task.to_dict() if updated_task else None,
    }


def get_tasks_by_priority(priority: Optional[str] = None) -> Dict:
    """
    Get tasks filtered by priority level.
    
    Args:
        priority: Filter by priority - "high", "medium", "low", or None for all
    
    Returns:
        Dictionary with list of tasks matching the priority
    """
    all_tasks = task_manager.get_all_tasks()
    
    if priority:
        priority = priority.lower()
        filtered_tasks = [task for task in all_tasks if task.priority == priority]
    else:
        filtered_tasks = all_tasks
    
    return {
        "count": len(filtered_tasks),
        "priority": priority or "all",
        "tasks": [task.to_dict() for task in filtered_tasks],
    }


def get_all_tasks(
    status: Optional[str] = None,
    assignee: Optional[str] = None,
    tag: Optional[str] = None,
) -> Dict:
    """
    Get all tasks with optional filtering by status, assignee, or tag.
    
    Args:
        status: Filter by status - "todo", "in_progress", "completed", or None for all
        assignee: Filter by assignee name, or None for all
        tag: Filter by tag, or None for all
    
    Returns:
        Dictionary with filtered list of tasks
    """
    all_tasks = task_manager.get_all_tasks()
    filtered_tasks = all_tasks
    
    if status:
        filtered_tasks = [t for t in filtered_tasks if t.status == status.lower()]
    
    if assignee:
        filtered_tasks = [t for t in filtered_tasks if t.assignee.lower() == assignee.lower()]
    
    if tag:
        filtered_tasks = [t for t in filtered_tasks if tag.lower() in [tg.lower() for tg in t.tags]]
    
    return {
        "count": len(filtered_tasks),
        "filters": {
            "status": status,
            "assignee": assignee,
            "tag": tag,
        },
        "tasks": [task.to_dict() for task in filtered_tasks],
    }


def delete_task(task_id: str) -> Dict:
    """
    Delete a task from the database.
    
    Args:
        task_id: The unique identifier of the task to delete
    
    Returns:
        Dictionary with deletion confirmation
    """
    task = task_manager.get_task(task_id)
    if not task:
        return {
            "status": "error",
            "message": f"Task with ID {task_id} not found",
        }
    
    success = task_manager.delete_task(task_id)
    
    if success:
        return {
            "status": "success",
            "message": f"Task {task_id} deleted successfully",
        }
    else:
        return {
            "status": "error",
            "message": f"Failed to delete task {task_id}",
        }


def calculate_productivity_metrics(assignee: Optional[str] = None, days: int = 30) -> Dict:
    """
    Calculate productivity metrics including completion rate, tasks by status, and average completion time.
    
    Args:
        assignee: Filter metrics for specific assignee, or None for all
        days: Number of days to look back for metrics (default: 30)
    
    Returns:
        Dictionary with productivity metrics
    """
    all_tasks = task_manager.get_all_tasks()
    
    if assignee:
        tasks = [t for t in all_tasks if t.assignee.lower() == assignee.lower()]
    else:
        tasks = all_tasks
    
    cutoff_date = datetime.now() - timedelta(days=days)
    
    recent_tasks = [t for t in tasks if t.created_at >= cutoff_date]
    
    total_tasks = len(recent_tasks)
    completed_tasks = len([t for t in recent_tasks if t.status == "completed"])
    in_progress_tasks = len([t for t in recent_tasks if t.status == "in_progress"])
    todo_tasks = len([t for t in recent_tasks if t.status == "todo"])
    
    completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    
    completed_with_dates = [
        t for t in recent_tasks
        if t.status == "completed" and t.completed_at and t.created_at
    ]
    
    avg_completion_time = None
    if completed_with_dates:
        completion_times = [
            (t.completed_at - t.created_at).total_seconds() / 3600
            for t in completed_with_dates
        ]
        avg_completion_time = sum(completion_times) / len(completion_times)
    
    high_priority_tasks = len([t for t in recent_tasks if t.priority == "high"])
    medium_priority_tasks = len([t for t in recent_tasks if t.priority == "medium"])
    low_priority_tasks = len([t for t in recent_tasks if t.priority == "low"])
    
    return {
        "period_days": days,
        "assignee": assignee or "all",
        "total_tasks": total_tasks,
        "status_breakdown": {
            "completed": completed_tasks,
            "in_progress": in_progress_tasks,
            "todo": todo_tasks,
        },
        "priority_breakdown": {
            "high": high_priority_tasks,
            "medium": medium_priority_tasks,
            "low": low_priority_tasks,
        },
        "completion_rate": round(completion_rate, 2),
        "average_completion_hours": round(avg_completion_time, 2) if avg_completion_time else None,
    }

