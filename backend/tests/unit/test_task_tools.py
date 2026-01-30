"""
Unit tests for task management tools
"""
import pytest
from tools.task_tools import (
    create_task,
    update_task_status,
    get_tasks_by_priority,
    calculate_productivity_metrics,
    get_all_tasks,
)

class TestTaskTools:
    """Test task management tools"""
    
    def test_create_task(self, task_manager, monkeypatch):
        """Test create_task tool"""
        monkeypatch.setattr("tools.task_tools.task_manager", task_manager)
        
        result = create_task(
            title="New Task",
            description="Test description",
            priority="high",
            deadline="2 days"
        )
        
        assert result["status"] == "success"
        assert "task_id" in result
        assert result["task"]["title"] == "New Task"
        assert result["task"]["priority"] == "high"
    
    def test_update_task_status(self, populated_task_manager, monkeypatch):
        """Test update_task_status tool"""
        monkeypatch.setattr("tools.task_tools.task_manager", populated_task_manager)
        
        result = update_task_status("TEST001", "in_progress")
        
        assert result["status"] == "success"
        assert result["task"]["status"] == "in_progress"
    
    def test_get_tasks_by_priority(self, populated_task_manager, monkeypatch):
        """Test get_tasks_by_priority tool"""
        monkeypatch.setattr("tools.task_tools.task_manager", populated_task_manager)
        
        result = get_tasks_by_priority("high")
        
        assert result["count"] == 1
        assert result["priority"] == "high"
        assert result["tasks"][0]["priority"] == "high"
    
    def test_get_all_tasks(self, populated_task_manager, monkeypatch):
        """Test get_all_tasks tool"""
        monkeypatch.setattr("tools.task_tools.task_manager", populated_task_manager)
        
        result = get_all_tasks()
        
        assert result["count"] == 3
        assert len(result["tasks"]) == 3
    
    def test_get_all_tasks_with_filters(self, populated_task_manager, monkeypatch):
        """Test get_all_tasks with filters"""
        monkeypatch.setattr("tools.task_tools.task_manager", populated_task_manager)
        
        result = get_all_tasks(status="completed")
        assert result["count"] == 1
        assert result["tasks"][0]["status"] == "completed"
        
        result = get_all_tasks(tag="urgent")
        assert result["count"] == 1
    
    def test_calculate_productivity_metrics(self, populated_task_manager, monkeypatch):
        """Test calculate_productivity_metrics tool"""
        monkeypatch.setattr("tools.task_tools.task_manager", populated_task_manager)
        
        result = calculate_productivity_metrics(days=30)
        
        assert "total_tasks" in result
        assert "completion_rate" in result
        assert "status_breakdown" in result
        assert "priority_breakdown" in result
        assert result["total_tasks"] == 3
        assert result["status_breakdown"]["completed"] == 1

