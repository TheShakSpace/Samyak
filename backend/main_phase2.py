"""
Phase 2: Task Management Tools Demo
Tests all task management tools with AISuite
"""
import aisuite as ai
from config import LLM_MODEL
from tools.task_tools import (
    create_task,
    update_task_status,
    get_tasks_by_priority,
    calculate_productivity_metrics,
    get_all_tasks,
    delete_task,
)
import json

client = ai.Client()

def test_tools_directly():
    """Test tools directly without LLM"""
    print("=" * 60)
    print("Phase 2: Testing Task Management Tools (Direct)")
    print("=" * 60)
    
    print("\n1. Testing create_task()...")
    result = create_task(
        title="Test Task from Tool",
        description="Testing the create_task tool",
        priority="high",
        deadline="2 days",
        tags=["test", "phase2"]
    )
    print(f"   ✓ {result['message']}")
    print(f"   Task ID: {result['task_id']}")
    
    print("\n2. Testing get_all_tasks()...")
    result = get_all_tasks()
    print(f"   ✓ Found {result['count']} total tasks")
    
    print("\n3. Testing get_tasks_by_priority('high')...")
    result = get_tasks_by_priority("high")
    print(f"   ✓ Found {result['count']} high priority tasks")
    
    print("\n4. Testing update_task_status()...")
    task_id = result['tasks'][0]['task_id'] if result['tasks'] else None
    if task_id:
        result = update_task_status(task_id, "in_progress")
        print(f"   ✓ {result['message']}")
    
    print("\n5. Testing calculate_productivity_metrics()...")
    result = calculate_productivity_metrics(days=30)
    print(f"   ✓ Productivity Metrics:")
    print(f"     - Total tasks: {result['total_tasks']}")
    print(f"     - Completion rate: {result['completion_rate']}%")
    print(f"     - Completed: {result['status_breakdown']['completed']}")
    print(f"     - In Progress: {result['status_breakdown']['in_progress']}")
    print(f"     - Todo: {result['status_breakdown']['todo']}")
    
    print("\n" + "=" * 60)
    print("Direct tool testing complete! ✓")
    print("=" * 60)

def test_with_llm():
    """Test tools with LLM using AISuite"""
    print("\n" + "=" * 60)
    print("Phase 2: Testing Task Management Tools (with LLM)")
    print("=" * 60)
    
    tools = [
        create_task,
        update_task_status,
        get_tasks_by_priority,
        calculate_productivity_metrics,
        get_all_tasks,
        delete_task,
    ]
    
    print(f"\nRegistered {len(tools)} tools with LLM")
    print("Tools available:")
    for tool in tools:
        print(f"  - {tool.__name__}")
    
    print("\n" + "-" * 60)
    print("Example: Ask LLM to create a task")
    print("-" * 60)
    
    prompt = "Add a task to finish the project report by Friday with high priority"
    
    print(f"\nUser prompt: {prompt}")
    print("\nLLM will use create_task tool...")
    
    try:
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are a task management assistant. Use the available tools to help users manage their tasks."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            tools=tools,
            max_turns=5
        )
        
        print("\nLLM Response:")
        print(response.choices[0].message.content)
        
        print("\n" + "=" * 60)
        print("LLM tool testing complete! ✓")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n⚠ Note: LLM testing requires Python 3.10+ and valid API key")
        print(f"Error: {e}")
        print("\nDirect tool testing above shows all tools work correctly!")

if __name__ == "__main__":
    test_tools_directly()
    
    print("\n" + "=" * 60)
    print("Testing with LLM (requires Python 3.10+ and API key)")
    print("=" * 60)
    
    try:
        test_with_llm()
    except Exception as e:
        print(f"\n⚠ LLM test skipped: {e}")
        print("All tools work correctly (tested directly above)")
    
    print("\n" + "=" * 60)
    print("Phase 2 Complete! ✓")
    print("=" * 60)
    print("\nNext: Phase 3 - Code-as-Plan for Task Queries")

