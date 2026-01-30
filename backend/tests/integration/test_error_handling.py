"""
Integration tests for error handling
"""
import pytest
from tools.task_tools import update_task_status, delete_task, get_tasks_by_priority
from tools.email_tools import send_task_reminder
from utils.code_executor import SafeCodeExecutor
from models.task import TaskManager

class TestErrorHandling:
    """Test error handling across components"""
    
    def test_update_nonexistent_task(self, task_manager, monkeypatch):
        """Test updating a non-existent task"""
        monkeypatch.setattr("tools.task_tools.task_manager", task_manager)
        
        result = update_task_status("NONEXISTENT", "completed")
        assert result["status"] == "error"
        assert "not found" in result["message"].lower()
    
    def test_delete_nonexistent_task(self, task_manager, monkeypatch):
        """Test deleting a non-existent task"""
        monkeypatch.setattr("tools.task_tools.task_manager", task_manager)
        
        result = delete_task("NONEXISTENT")
        assert result["status"] == "error"
        assert "not found" in result["message"].lower()
    
    def test_invalid_task_status(self, populated_task_manager, monkeypatch):
        """Test updating with invalid status"""
        monkeypatch.setattr("tools.task_tools.task_manager", populated_task_manager)
        
        result = update_task_status("TEST001", "invalid_status")
        assert result["status"] == "error"
        assert "invalid" in result["message"].lower()
    
    def test_code_executor_error_handling(self, task_manager):
        """Test code executor handles errors"""
        executor = SafeCodeExecutor(task_manager)
        
        error_code = """
# This will cause an error
undefined_variable = non_existent_function()
"""
        
        result = executor.execute(error_code)
        assert result["error"] is not None
        assert "answer" in result
    
    def test_email_without_config(self, populated_task_manager, monkeypatch):
        """Test email without configuration"""
        monkeypatch.setattr("tools.email_tools.task_manager", populated_task_manager)
        monkeypatch.setattr("tools.email_tools.email_service.enabled", False)
        
        result = send_task_reminder("test@example.com", days_ahead=1)
        assert result["email_sent"] == False
        assert "not configured" in result["message"].lower() or result["status"] == "error"
    
    def test_empty_query_results(self, task_manager, monkeypatch):
        """Test queries with no results"""
        monkeypatch.setattr("tools.task_tools.task_manager", task_manager)
        
        result = get_tasks_by_priority("high")
        assert result["count"] == 0
        assert len(result["tasks"]) == 0

