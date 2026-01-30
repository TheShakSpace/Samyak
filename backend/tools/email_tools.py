from typing import List, Optional, Dict
from datetime import datetime, timedelta
from models.task import TaskManager, Task
from config import TASKS_DB_PATH, EMAIL_CONFIG
from utils.email_service import EmailService
from tools.task_tools import calculate_productivity_metrics
from templates.email_templates import (
    format_task_reminder_email,
    format_productivity_summary_email,
    format_task_completion_email,
)

task_manager = TaskManager(TASKS_DB_PATH)
email_service = EmailService()

def send_task_reminder(
    to_address: str,
    days_ahead: int = 1,
    assignee: Optional[str] = None
) -> Dict:
    """
    Send a reminder email for tasks due soon.
    
    Args:
        to_address: Recipient email address
        days_ahead: How many days ahead to check (default: 1 for tomorrow)
        assignee: Filter by assignee, or None for all
    
    Returns:
        Dictionary with send status and task details
    """
    all_tasks = task_manager.get_all_tasks()
    
    cutoff_date = datetime.now() + timedelta(days=days_ahead)
    start_date = datetime.now()
    
    upcoming_tasks = [
        t for t in all_tasks
        if t.deadline
        and t.deadline >= start_date
        and t.deadline <= cutoff_date
        and t.status != "completed"
    ]
    
    if assignee:
        upcoming_tasks = [t for t in upcoming_tasks if t.assignee.lower() == assignee.lower()]
    
    if not upcoming_tasks:
        return {
            "status": "success",
            "message": f"No tasks due in the next {days_ahead} day(s)",
            "tasks_count": 0,
            "email_sent": False
        }
    
    subject, body = format_task_reminder_email(upcoming_tasks, days_ahead)
    result = email_service.send_email(to_address, subject, body)
    
    return {
        "status": result["status"],
        "message": result["message"],
        "tasks_count": len(upcoming_tasks),
        "tasks": [t.to_dict() for t in upcoming_tasks],
        "email_sent": result.get("sent", False)
    }

def send_productivity_summary(
    to_address: str,
    period_days: int = 7,
    assignee: Optional[str] = None
) -> Dict:
    """
    Send a productivity summary email with metrics.
    
    Args:
        to_address: Recipient email address
        period_days: Number of days to include in summary (default: 7)
        assignee: Filter by assignee, or None for all
    
    Returns:
        Dictionary with send status and metrics
    """
    metrics = calculate_productivity_metrics(assignee=assignee, days=period_days)
    
    subject, body = format_productivity_summary_email(metrics, period_days)
    result = email_service.send_email(to_address, subject, body)
    
    return {
        "status": result["status"],
        "message": result["message"],
        "metrics": metrics,
        "email_sent": result.get("sent", False)
    }

def send_task_completion_notification(
    to_address: str,
    task_id: str
) -> Dict:
    """
    Send an email notification when a task is completed.
    
    Args:
        to_address: Recipient email address
        task_id: ID of the completed task
    
    Returns:
        Dictionary with send status
    """
    task = task_manager.get_task(task_id)
    
    if not task:
        return {
            "status": "error",
            "message": f"Task with ID {task_id} not found",
            "email_sent": False
        }
    
    if task.status != "completed":
        return {
            "status": "error",
            "message": f"Task {task_id} is not completed",
            "email_sent": False
        }
    
    subject, body = format_task_completion_email(task)
    result = email_service.send_email(to_address, subject, body)
    
    return {
        "status": result["status"],
        "message": result["message"],
        "task": task.to_dict(),
        "email_sent": result.get("sent", False)
    }

def send_custom_email(
    to_address: str,
    subject: str,
    body: str
) -> Dict:
    """
    Send a custom email message.
    
    Args:
        to_address: Recipient email address
        subject: Email subject
        body: Email body content
    
    Returns:
        Dictionary with send status
    """
    result = email_service.send_email(to_address, subject, body)
    
    return {
        "status": result["status"],
        "message": result["message"],
        "email_sent": result.get("sent", False)
    }

def get_upcoming_tasks_for_reminder(
    days_ahead: int = 1,
    assignee: Optional[str] = None
) -> Dict:
    """
    Get tasks that are due soon (for reminder purposes).
    This is a helper function that doesn't send email, just returns the tasks.
    
    Args:
        days_ahead: How many days ahead to check
        assignee: Filter by assignee, or None for all
    
    Returns:
        Dictionary with list of upcoming tasks
    """
    all_tasks = task_manager.get_all_tasks()
    
    cutoff_date = datetime.now() + timedelta(days=days_ahead)
    start_date = datetime.now()
    
    upcoming_tasks = [
        t for t in all_tasks
        if t.deadline
        and t.deadline >= start_date
        and t.deadline <= cutoff_date
        and t.status != "completed"
    ]
    
    if assignee:
        upcoming_tasks = [t for t in upcoming_tasks if t.assignee.lower() == assignee.lower()]
    
    return {
        "count": len(upcoming_tasks),
        "days_ahead": days_ahead,
        "assignee": assignee or "all",
        "tasks": [t.to_dict() for t in upcoming_tasks]
    }

