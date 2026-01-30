import aisuite as ai
from config import TASKS_DB_PATH, LLM_MODEL
from models.task import TaskManager, Task
from datetime import datetime, timedelta
import json

client = ai.Client()
task_manager = TaskManager(TASKS_DB_PATH)

def create_sample_tasks():
    sample_tasks = [
        Task(
            task_id="TASK001",
            title="Finish project report",
            description="Complete the quarterly project report with all metrics",
            priority="high",
            deadline=datetime.now() + timedelta(days=2),
            status="in_progress",
            assignee="me",
            tags=["work", "urgent"]
        ),
        Task(
            task_id="TASK002",
            title="Review code changes",
            description="Review pull requests from the team",
            priority="medium",
            deadline=datetime.now() + timedelta(days=5),
            status="todo",
            assignee="me",
            tags=["work", "code"]
        ),
        Task(
            task_id="TASK003",
            title="Team meeting preparation",
            description="Prepare agenda and materials for weekly team meeting",
            priority="high",
            deadline=datetime.now() + timedelta(days=1),
            status="todo",
            assignee="me",
            tags=["work", "meeting"]
        ),
    ]
    
    for task in sample_tasks:
        existing = task_manager.get_task(task.task_id)
        if not existing:
            task_manager.add_task(task)
    
    print(f"Created {len(sample_tasks)} sample tasks")
    return sample_tasks

if __name__ == "__main__":
    print("Task Management Agent - Phase 1 Setup")
    print("=" * 50)
    
    print("\n1. Initializing AISuite client...")
    print(f"   Model: {LLM_MODEL}")
    
    print("\n2. Creating sample tasks...")
    sample_tasks = create_sample_tasks()
    
    print("\n3. Verifying task storage...")
    all_tasks = task_manager.get_all_tasks()
    print(f"   Total tasks in database: {len(all_tasks)}")
    
    print("\n4. Sample task data:")
    if all_tasks:
        sample = all_tasks[0]
        print(json.dumps(sample.to_dict(), indent=2))
    
    print("\n" + "=" * 50)
    print("Phase 1 Complete! Ready for Phase 2 (Tool Implementation)")

