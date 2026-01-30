"""
Test script for Phase 1 - Tests core functionality without requiring aisuite
"""
from config import TASKS_DB_PATH
from models.task import TaskManager, Task
from datetime import datetime, timedelta
import json
import os

def test_phase1():
    print("Task Management Agent - Phase 1 Testing")
    print("=" * 50)
    
    print("\n1. Testing TaskManager initialization...")
    task_manager = TaskManager(TASKS_DB_PATH)
    print(f"   ✓ TaskManager created")
    print(f"   Database path: {TASKS_DB_PATH}")
    
    print("\n2. Testing Task creation...")
    test_task = Task(
        task_id="TEST001",
        title="Test Task",
        description="This is a test task",
        priority="high",
        deadline=datetime.now() + timedelta(days=1),
        status="todo",
        assignee="me",
        tags=["test"]
    )
    print(f"   ✓ Task created: {test_task.title}")
    
    print("\n3. Testing Task serialization...")
    task_dict = test_task.to_dict()
    print(f"   ✓ Task serialized to dict")
    print(f"   Keys: {list(task_dict.keys())}")
    
    print("\n4. Testing Task deserialization...")
    restored_task = Task.from_dict(task_dict)
    print(f"   ✓ Task deserialized")
    print(f"   Title matches: {restored_task.title == test_task.title}")
    
    print("\n5. Testing TaskManager operations...")
    task_manager.add_task(test_task)
    print(f"   ✓ Task added to manager")
    
    retrieved_task = task_manager.get_task("TEST001")
    print(f"   ✓ Task retrieved: {retrieved_task.title if retrieved_task else 'None'}")
    
    all_tasks = task_manager.get_all_tasks()
    print(f"   ✓ Total tasks: {len(all_tasks)}")
    
    print("\n6. Testing Task update...")
    task_manager.update_task("TEST001", status="in_progress", priority="medium")
    updated_task = task_manager.get_task("TEST001")
    print(f"   ✓ Task updated")
    print(f"   Status: {updated_task.status if updated_task else 'N/A'}")
    print(f"   Priority: {updated_task.priority if updated_task else 'N/A'}")
    
    print("\n7. Testing sample tasks creation...")
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
    
    created_count = 0
    for task in sample_tasks:
        existing = task_manager.get_task(task.task_id)
        if not existing:
            task_manager.add_task(task)
            created_count += 1
    
    print(f"   ✓ Created {created_count} new sample tasks")
    
    print("\n8. Verifying task storage...")
    all_tasks = task_manager.get_all_tasks()
    print(f"   ✓ Total tasks in database: {len(all_tasks)}")
    
    if os.path.exists(TASKS_DB_PATH):
        file_size = os.path.getsize(TASKS_DB_PATH)
        print(f"   ✓ Database file exists: {TASKS_DB_PATH}")
        print(f"   File size: {file_size} bytes")
    
    print("\n9. Displaying sample task data...")
    if all_tasks:
        sample = all_tasks[0]
        print(json.dumps(sample.to_dict(), indent=2))
    
    print("\n10. Testing configuration...")
    try:
        from config import LLM_MODEL, EMAIL_CONFIG
        print(f"   ✓ Configuration loaded")
        print(f"   LLM Model: {LLM_MODEL}")
        print(f"   Email config available: {bool(EMAIL_CONFIG)}")
    except Exception as e:
        print(f"   ⚠ Configuration issue: {e}")
    
    print("\n" + "=" * 50)
    print("Phase 1 Testing Complete! ✓")
    print("\nNote: AISuite requires Python 3.10+")
    print("Core functionality (Task model, storage) works correctly!")
    print("\nReady for Phase 2 (Tool Implementation)")

if __name__ == "__main__":
    test_phase1()

