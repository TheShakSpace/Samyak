"""
Unit tests for Task model and TaskManager
"""
import pytest
from datetime import datetime, timedelta
from models.task import Task, TaskManager

class TestTask:
    """Test Task model"""
    
    def test_task_creation(self):
        """Test creating a task"""
        task = Task(
            task_id="T001",
            title="Test Task",
            description="Test description",
            priority="high"
        )
        assert task.task_id == "T001"
        assert task.title == "Test Task"
        assert task.priority == "high"
        assert task.status == "todo"
    
    def test_task_serialization(self):
        """Test task serialization to dict"""
        task = Task(
            task_id="T001",
            title="Test Task",
            deadline=datetime.now() + timedelta(days=1)
        )
        task_dict = task.to_dict()
        assert task_dict["task_id"] == "T001"
        assert task_dict["title"] == "Test Task"
        assert "deadline" in task_dict
    
    def test_task_deserialization(self):
        """Test task deserialization from dict"""
        task_dict = {
            "task_id": "T001",
            "title": "Test Task",
            "description": "Test",
            "priority": "high",
            "deadline": (datetime.now() + timedelta(days=1)).isoformat(),
            "status": "todo",
            "assignee": "me",
            "tags": ["test"],
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "completed_at": None
        }
        task = Task.from_dict(task_dict)
        assert task.task_id == "T001"
        assert task.title == "Test Task"
        assert task.priority == "high"

class TestTaskManager:
    """Test TaskManager"""
    
    def test_task_manager_initialization(self, task_manager):
        """Test TaskManager initialization"""
        assert task_manager is not None
        assert len(task_manager.get_all_tasks()) == 0
    
    def test_add_task(self, task_manager):
        """Test adding a task"""
        task = Task(task_id="T001", title="Test Task")
        task_manager.add_task(task)
        assert len(task_manager.get_all_tasks()) == 1
    
    def test_get_task(self, populated_task_manager):
        """Test getting a task by ID"""
        task = populated_task_manager.get_task("TEST001")
        assert task is not None
        assert task.task_id == "TEST001"
        assert task.title == "Test Task 1"
    
    def test_update_task(self, populated_task_manager):
        """Test updating a task"""
        updated = populated_task_manager.update_task("TEST001", status="in_progress")
        assert updated is not None
        assert updated.status == "in_progress"
        
        task = populated_task_manager.get_task("TEST001")
        assert task.status == "in_progress"
    
    def test_delete_task(self, populated_task_manager):
        """Test deleting a task"""
        result = populated_task_manager.delete_task("TEST001")
        assert result is True
        
        task = populated_task_manager.get_task("TEST001")
        assert task is None
        
        assert len(populated_task_manager.get_all_tasks()) == 2
    
    def test_get_all_tasks(self, populated_task_manager):
        """Test getting all tasks"""
        all_tasks = populated_task_manager.get_all_tasks()
        assert len(all_tasks) == 3

