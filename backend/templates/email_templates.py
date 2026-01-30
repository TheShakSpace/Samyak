from typing import List
from datetime import datetime
from models.task import Task

def format_task_reminder_email(tasks: List[Task], days_ahead: int = 1) -> tuple[str, str]:
    """
    Format a task reminder email.
    
    Args:
        tasks: List of tasks to remind about
        days_ahead: How many days ahead
    
    Returns:
        Tuple of (subject, body)
    """
    subject = f"Task Reminder: {len(tasks)} task(s) due soon"
    
    body = f"""Task Reminder

You have {len(tasks)} task(s) due in the next {days_ahead} day(s):

"""
    for i, task in enumerate(tasks, 1):
        deadline_str = task.deadline.strftime("%Y-%m-%d %H:%M") if task.deadline else "No deadline"
        body += f"{i}. {task.title}\n"
        body += f"   Priority: {task.priority.upper()}\n"
        body += f"   Status: {task.status.replace('_', ' ').title()}\n"
        body += f"   Deadline: {deadline_str}\n"
        if task.description:
            desc = task.description[:100] + "..." if len(task.description) > 100 else task.description
            body += f"   Description: {desc}\n"
        if task.tags:
            body += f"   Tags: {', '.join(task.tags)}\n"
        body += "\n"
    
    body += "\n---\nTask Management Agent"
    
    return subject, body

def format_productivity_summary_email(metrics: dict, period_days: int = 7) -> tuple[str, str]:
    """
    Format a productivity summary email.
    
    Args:
        metrics: Productivity metrics dictionary
        period_days: Number of days the summary covers
    
    Returns:
        Tuple of (subject, body)
    """
    subject = f"Productivity Summary - Last {period_days} Days"
    
    completion_rate = metrics.get("completion_rate", 0)
    total_tasks = metrics.get("total_tasks", 0)
    status_breakdown = metrics.get("status_breakdown", {})
    priority_breakdown = metrics.get("priority_breakdown", {})
    
    body = f"""Productivity Summary

Period: Last {period_days} days

📊 Overview:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Tasks: {total_tasks}
Completion Rate: {completion_rate}%

Status Breakdown:
  ✓ Completed: {status_breakdown.get("completed", 0)}
  🔄 In Progress: {status_breakdown.get("in_progress", 0)}
  📋 To Do: {status_breakdown.get("todo", 0)}

Priority Breakdown:
  🔴 High: {priority_breakdown.get("high", 0)}
  🟡 Medium: {priority_breakdown.get("medium", 0)}
  🟢 Low: {priority_breakdown.get("low", 0)}
"""
    
    if metrics.get("average_completion_hours"):
        body += f"\n⏱️  Average Completion Time: {metrics['average_completion_hours']} hours\n"
    
    body += "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    body += "Task Management Agent"
    
    return subject, body

def format_task_completion_email(task: Task) -> tuple[str, str]:
    """
    Format an email notification for task completion.
    
    Args:
        task: Completed task
    
    Returns:
        Tuple of (subject, body)
    """
    subject = f"Task Completed: {task.title}"
    
    body = f"""Task Completed! 🎉

Great job completing your task!

Task Details:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Title: {task.title}
Priority: {task.priority.upper()}
Completed At: {task.completed_at.strftime("%Y-%m-%d %H:%M") if task.completed_at else "N/A"}

"""
    if task.description:
        body += f"Description: {task.description}\n\n"
    
    if task.tags:
        body += f"Tags: {', '.join(task.tags)}\n\n"
    
    body += "Keep up the great work!\n"
    body += "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    body += "Task Management Agent"
    
    return subject, body

