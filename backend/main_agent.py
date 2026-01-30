"""
Main Agent Entry Point
Unified interface for the Task Management & Productivity Agent
"""
from agent.orchestrator import TaskManagementAgent
from agent.router import RequestRouter
import json

def print_response(response: dict):
    """Pretty print agent response"""
    print("\n" + "=" * 60)
    print("Agent Response")
    print("=" * 60)
    
    if response.get('status') == 'success':
        print(f"\n✓ Status: {response['status']}")
        if response.get('response'):
            print(f"\nResponse:\n{response['response']}")
        if response.get('tools_used'):
            print(f"\nTools Used: {response['tools_used']}")
    elif response.get('status') == 'info':
        print(f"\nℹ Status: {response['status']}")
        print(f"\nMessage: {response['message']}")
        if response.get('suggestion'):
            print(f"\nSuggestion: {response['suggestion']}")
    else:
        print(f"\n✗ Status: {response['status']}")
        print(f"\nMessage: {response['message']}")
        if response.get('error'):
            print(f"\nError: {response['error']}")
    
    if response.get('routing'):
        routing = response['routing']
        print(f"\nRequest Analysis:")
        print(f"  Categories: {', '.join(routing['categories'])}")
        print(f"  Recommended Tools: {', '.join(routing['recommended_tools'])}")
        print(f"  Complexity: {routing['complexity']}")
    
    print("\n" + "=" * 60)

def main():
    """Main entry point for the agent"""
    print("=" * 60)
    print("Task Management & Productivity Agent")
    print("=" * 60)
    
    agent = TaskManagementAgent()
    
    print("\n1. System Status:")
    status = agent.get_system_status()
    print(f"   LLM Available: {status['llm_available']}")
    print(f"   Model: {status['model'] or 'N/A'}")
    print(f"   Total Tools: {status['total_tools']}")
    print(f"   Total Tasks: {status['total_tasks']}")
    
    print("\n2. Available Capabilities:")
    for capability, available in status['capabilities'].items():
        symbol = "✓" if available else "✗"
        print(f"   {symbol} {capability.replace('_', ' ').title()}")
    
    print("\n3. Example Requests:")
    examples = [
        "Add a task to finish the project report by Friday with high priority",
        "Show me all high priority tasks",
        "Create a chart showing my task completion rate",
        "Send me a reminder email for tasks due tomorrow",
        "What's my productivity metrics for the last week?",
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"   {i}. {example}")
    
    print("\n" + "=" * 60)
    print("Agent Ready!")
    print("=" * 60)
    
    if not status['llm_available']:
        print("\n⚠ Note: LLM processing requires Python 3.10+ and aisuite")
        print("All tools are available for direct use.")
        print("\nExample: Direct tool usage")
        print("-" * 60)
        from tools.task_tools import create_task, get_all_tasks
        
        result = create_task(
            title="Test task from agent",
            description="Testing direct tool usage",
            priority="medium"
        )
        print(f"Created task: {result['message']}")
        
        all_tasks = get_all_tasks()
        print(f"Total tasks: {all_tasks['count']}")
    else:
        print("\n✓ LLM processing available!")
        print("You can now use natural language requests.")
        print("\nExample: Natural language request")
        print("-" * 60)
        
        request = "Show me all my tasks"
        response = agent.process_request(request)
        print_response(response)

if __name__ == "__main__":
    main()

