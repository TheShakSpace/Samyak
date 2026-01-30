"""
Pytest configuration and fixtures
"""
import pytest
import json
import tempfile
import shutil
from pathlib import Path
from datetime import datetime, timedelta
from models.task import TaskManager, Task
from config import TASKS_DB_PATH

@pytest.fixture
def temp_db_path():
    """Create a temporary database file for testing"""
    temp_dir = tempfile.mkdtemp()
    db_path = Path(temp_dir) / "test_tasks.json"
    yield str(db_path)
    shutil.rmtree(temp_dir)

@pytest.fixture
def task_manager(temp_db_path):
    """Create a TaskManager instance with temporary database"""
    return TaskManager(temp_db_path)

@pytest.fixture
def sample_tasks():
    """Create sample tasks for testing"""
    now = datetime.now()
    return [
        Task(
            task_id="TEST001",
            title="Test Task 1",
            description="First test task",
            priority="high",
            deadline=now + timedelta(days=1),
            status="todo",
            assignee="test_user",
            tags=["test", "urgent"]
        ),
        Task(
            task_id="TEST002",
            title="Test Task 2",
            description="Second test task",
            priority="medium",
            deadline=now + timedelta(days=3),
            status="in_progress",
            assignee="test_user",
            tags=["test"]
        ),
        Task(
            task_id="TEST003",
            title="Test Task 3",
            description="Third test task",
            priority="low",
            deadline=now + timedelta(days=7),
            status="completed",
            assignee="test_user",
            tags=["test", "done"],
            completed_at=now - timedelta(days=1)
        ),
    ]

@pytest.fixture
def populated_task_manager(task_manager, sample_tasks):
    """Create a TaskManager with sample tasks"""
    for task in sample_tasks:
        task_manager.add_task(task)
    return task_manager

@pytest.fixture
def mock_email_config(monkeypatch):
    """Mock email configuration"""
    monkeypatch.setenv("EMAIL_ADDRESS", "test@example.com")
    monkeypatch.setenv("EMAIL_PASSWORD", "test_password")
    monkeypatch.setenv("SMTP_SERVER", "smtp.test.com")
    monkeypatch.setenv("SMTP_PORT", "587")

