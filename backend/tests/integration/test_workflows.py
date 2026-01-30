"""
Integration tests for end-to-end workflows
"""
import pytest
from datetime import datetime, timedelta
from tools.task_tools import create_task, update_task_status, get_all_tasks, calculate_productivity_metrics
from tools.email_tools import get_upcoming_tasks_for_reminder
from tools.visualization_tools import create_priority_distribution_chart
from agent.router import RequestRouter
from agent.orchestrator import TaskManagementAgent

class TestWorkflows:
    """Test end-to-end workflows"""
    
    def test_task_lifecycle_workflow(self, task_manager, monkeypatch):
        """Test complete task lifecycle"""
        monkeypatch.setattr("tools.task_tools.task_manager", task_manager)
        monkeypatch.setattr("tools.email_tools.task_manager", task_manager)
        
        # Create task
        create_result = create_task(
            title="Workflow Test Task",
            priority="high",
            deadline="1 day"
        )
        task_id = create_result["task_id"]
        assert create_result["status"] == "success"
        
        # Update status
        update_result = update_task_status(task_id, "in_progress")
        assert update_result["status"] == "success"
        
        # Complete task
        complete_result = update_task_status(task_id, "completed")
        assert complete_result["status"] == "success"
        
        # Verify
        all_tasks = get_all_tasks()
        task = next((t for t in all_tasks["tasks"] if t["task_id"] == task_id), None)
        assert task is not None
        assert task["status"] == "completed"
    
    def test_productivity_workflow(self, populated_task_manager, monkeypatch):
        """Test productivity metrics workflow"""
        monkeypatch.setattr("tools.task_tools.task_manager", populated_task_manager)
        
        # Get metrics
        metrics = calculate_productivity_metrics(days=30)
        
        assert metrics["total_tasks"] > 0
        assert "completion_rate" in metrics
        assert "status_breakdown" in metrics
        
        # Verify metrics are reasonable
        assert 0 <= metrics["completion_rate"] <= 100
        assert metrics["status_breakdown"]["completed"] >= 0
    
    def test_reminder_workflow(self, populated_task_manager, monkeypatch):
        """Test reminder workflow"""
        monkeypatch.setattr("tools.email_tools.task_manager", populated_task_manager)
        
        # Get upcoming tasks
        upcoming = get_upcoming_tasks_for_reminder(days_ahead=7)
        
        assert "count" in upcoming
        assert "tasks" in upcoming
        assert upcoming["count"] >= 0
    
    def test_chart_generation_workflow(self, populated_task_manager, monkeypatch, tmp_path):
        """Test chart generation workflow"""
        monkeypatch.setattr("tools.visualization_tools.task_manager", populated_task_manager)
        
        chart_path = str(tmp_path / "test_chart.png")
        result = create_priority_distribution_chart(output_path=chart_path)
        
        assert result["status"] == "success"
        assert result["chart_path"] == chart_path
    
    def test_request_routing_workflow(self):
        """Test request routing workflow"""
        router = RequestRouter()
        
        requests = [
            "Add a task",
            "Show high priority tasks",
            "Send reminder email",
            "Create completion chart"
        ]
        
        for request in requests:
            routing = router.route(request)
            assert "categories" in routing
            assert "recommended_tools" in routing
            assert len(routing["categories"]) > 0
            assert len(routing["recommended_tools"]) > 0
    
    def test_agent_initialization_workflow(self):
        """Test agent initialization workflow"""
        agent = TaskManagementAgent()
        
        assert agent is not None
        assert len(agent.tools) > 0
        
        status = agent.get_system_status()
        assert "llm_available" in status
        assert "total_tools" in status
        assert "capabilities" in status

