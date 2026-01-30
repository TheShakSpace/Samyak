import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional, Dict
from datetime import datetime, timedelta
from config import EMAIL_CONFIG
from models.task import TaskManager, Task
from config import TASKS_DB_PATH

class EmailService:
    """Service for sending emails via SMTP"""
    
    def __init__(self):
        self.smtp_server = EMAIL_CONFIG.get("smtp_server", "smtp.gmail.com")
        self.smtp_port = EMAIL_CONFIG.get("smtp_port", 587)
        self.email_address = EMAIL_CONFIG.get("email_address", "")
        self.email_password = EMAIL_CONFIG.get("email_password", "")
        self.enabled = bool(self.email_address and self.email_password)
    
    def send_email(
        self,
        to_address: str,
        subject: str,
        body: str,
        is_html: bool = False
    ) -> Dict:
        """
        Send an email via SMTP.
        
        Args:
            to_address: Recipient email address
            subject: Email subject
            body: Email body content
            is_html: Whether body is HTML format
        
        Returns:
            Dictionary with send status
        """
        if not self.enabled:
            return {
                "status": "error",
                "message": "Email service not configured. Please set EMAIL_ADDRESS and EMAIL_PASSWORD in .env",
                "sent": False
            }
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_address
            msg['To'] = to_address
            msg['Subject'] = subject
            
            if is_html:
                msg.attach(MIMEText(body, 'html'))
            else:
                msg.attach(MIMEText(body, 'plain'))
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_address, self.email_password)
                server.send_message(msg)
            
            return {
                "status": "success",
                "message": f"Email sent successfully to {to_address}",
                "sent": True
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to send email: {str(e)}",
                "sent": False,
                "error": str(e)
            }
    
    def send_reminder(
        self,
        to_address: str,
        tasks: List[Task],
        days_ahead: int = 1
    ) -> Dict:
        """
        Send a reminder email for upcoming tasks.
        
        Args:
            to_address: Recipient email address
            tasks: List of tasks to remind about
            days_ahead: How many days ahead to remind (default: 1)
        
        Returns:
            Dictionary with send status
        """
        if not tasks:
            return {
                "status": "success",
                "message": "No tasks to remind about",
                "sent": False
            }
        
        subject = f"Task Reminder: {len(tasks)} task(s) due soon"
        
        body = f"""Task Reminder

You have {len(tasks)} task(s) due in the next {days_ahead} day(s):

"""
        for task in tasks:
            deadline_str = task.deadline.strftime("%Y-%m-%d %H:%M") if task.deadline else "No deadline"
            body += f"- {task.title} (Priority: {task.priority}, Status: {task.status})\n"
            body += f"  Deadline: {deadline_str}\n"
            if task.description:
                body += f"  Description: {task.description[:100]}...\n"
            body += "\n"
        
        body += "\n---\nTask Management Agent"
        
        return self.send_email(to_address, subject, body)
    
    def send_productivity_summary(
        self,
        to_address: str,
        metrics: Dict,
        period_days: int = 7
    ) -> Dict:
        """
        Send a productivity summary email.
        
        Args:
            to_address: Recipient email address
            metrics: Productivity metrics dictionary
            period_days: Number of days the summary covers
        
        Returns:
            Dictionary with send status
        """
        subject = f"Productivity Summary - Last {period_days} Days"
        
        completion_rate = metrics.get("completion_rate", 0)
        total_tasks = metrics.get("total_tasks", 0)
        completed = metrics.get("status_breakdown", {}).get("completed", 0)
        in_progress = metrics.get("status_breakdown", {}).get("in_progress", 0)
        todo = metrics.get("status_breakdown", {}).get("todo", 0)
        
        body = f"""Productivity Summary

Period: Last {period_days} days

Overview:
- Total Tasks: {total_tasks}
- Completion Rate: {completion_rate}%
- Completed: {completed}
- In Progress: {in_progress}
- To Do: {todo}

Priority Breakdown:
- High Priority: {metrics.get("priority_breakdown", {}).get("high", 0)}
- Medium Priority: {metrics.get("priority_breakdown", {}).get("medium", 0)}
- Low Priority: {metrics.get("priority_breakdown", {}).get("low", 0)}

"""
        if metrics.get("average_completion_hours"):
            body += f"Average Completion Time: {metrics['average_completion_hours']} hours\n"
        
        body += "\n---\nTask Management Agent"
        
        return self.send_email(to_address, subject, body)

