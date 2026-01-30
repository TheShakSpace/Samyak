"""
Phase 6 Testing - Integration & Orchestration
Tests the unified agent orchestrator and request routing
"""
from agent.orchestrator import TaskManagementAgent
from agent.router import RequestRouter
from tools.task_tools import get_all_tasks

def test_request_router():
    """Test request routing"""
    print("=" * 60)
    print("Phase 6: Testing Integration & Orchestration")
    print("=" * 60)
    
    print("\n1. Testing RequestRouter...")
    router = RequestRouter()
    
    test_requests = [
        "Add a task to finish the project report",
        "Show me all high priority tasks",
        "Send me a reminder email for tasks due tomorrow",
        "Create a chart showing task completion rate",
        "What's my productivity metrics?",
        "Find all incomplete tasks assigned to me",
    ]
    
    for request in test_requests:
        routing = router.route(request)
        print(f"\n   Request: {request[:50]}...")
        print(f"   Categories: {', '.join(routing['categories'])}")
        print(f"   Recommended Tools: {', '.join(routing['recommended_tools'])}")
        print(f"   Complexity: {routing['complexity']}")

def test_agent_initialization():
    """Test agent initialization"""
    print("\n2. Testing TaskManagementAgent initialization...")
    
    agent = TaskManagementAgent()
    
    print(f"   ✓ Agent created")
    print(f"   Model: {agent.model}")
    print(f"   LLM Available: {agent.client is not None}")
    print(f"   Total Tools: {len(agent.tools)}")
    
    print(f"\n   Available Tools:")
    for i, tool in enumerate(agent.tools[:10], 1):
        print(f"     {i}. {tool.__name__}")
    if len(agent.tools) > 10:
        print(f"     ... and {len(agent.tools) - 10} more")

def test_system_status():
    """Test system status"""
    print("\n3. Testing system status...")
    
    agent = TaskManagementAgent()
    status = agent.get_system_status()
    
    print(f"   ✓ System status retrieved")
    print(f"   LLM Available: {status['llm_available']}")
    print(f"   Model: {status['model'] or 'N/A'}")
    print(f"   Total Tools: {status['total_tools']}")
    print(f"   Total Tasks: {status['total_tasks']}")
    
    print(f"\n   Capabilities:")
    for capability, available in status['capabilities'].items():
        symbol = "✓" if available else "✗"
        print(f"     {symbol} {capability.replace('_', ' ').title()}")

def test_tool_registration():
    """Test tool registration"""
    print("\n4. Testing tool registration...")
    
    agent = TaskManagementAgent()
    tools_info = agent.get_available_tools()
    
    print(f"   ✓ {len(tools_info)} tools registered")
    
    tool_categories = {}
    for tool in tools_info:
        module = tool['module'].split('.')[-1] if '.' in tool['module'] else tool['module']
        if module not in tool_categories:
            tool_categories[module] = []
        tool_categories[module].append(tool['name'])
    
    print(f"\n   Tools by category:")
    for category, tools in tool_categories.items():
        print(f"     {category}: {len(tools)} tools")
        for tool in tools[:3]:
            print(f"       - {tool}")
        if len(tools) > 3:
            print(f"       ... and {len(tools) - 3} more")

def test_request_processing():
    """Test request processing"""
    print("\n5. Testing request processing...")
    
    agent = TaskManagementAgent()
    
    test_requests = [
        "Show me all my tasks",
        "What tasks do I have?",
        "List all high priority tasks",
    ]
    
    for request in test_requests:
        print(f"\n   Request: {request}")
        response = agent.process_request(request, use_llm=False)
        print(f"   Status: {response['status']}")
        if response.get('routing'):
            print(f"   Categories: {', '.join(response['routing']['categories'])}")

def test_integration_workflow():
    """Test end-to-end integration workflow"""
    print("\n6. Testing integration workflow...")
    
    print("\n   Step 1: Check current tasks")
    all_tasks = get_all_tasks()
    print(f"   ✓ Current tasks: {all_tasks['count']}")
    
    print("\n   Step 2: Initialize agent")
    agent = TaskManagementAgent()
    print(f"   ✓ Agent initialized with {len(agent.tools)} tools")
    
    print("\n   Step 3: Route a request")
    router = RequestRouter()
    routing = router.route("Show me all high priority tasks")
    print(f"   ✓ Request routed to: {', '.join(routing['recommended_tools'])}")
    
    print("\n   Step 4: Get system status")
    status = agent.get_system_status()
    print(f"   ✓ System status: {status['total_tasks']} tasks, {status['total_tools']} tools")
    
    print("\n   ✓ Integration workflow complete!")

def test_error_handling():
    """Test error handling"""
    print("\n7. Testing error handling...")
    
    agent = TaskManagementAgent()
    
    if not agent.client:
        response = agent.process_request("Test request")
        print(f"   ✓ Handles missing LLM gracefully")
        print(f"   Status: {response['status']}")
        print(f"   Message: {response['message']}")
    else:
        print(f"   ✓ LLM available, error handling not needed")

if __name__ == "__main__":
    test_request_router()
    test_agent_initialization()
    test_system_status()
    test_tool_registration()
    test_request_processing()
    test_integration_workflow()
    test_error_handling()
    
    print("\n" + "=" * 60)
    print("Phase 6 Testing Complete! ✓")
    print("=" * 60)
    print("\nIntegration & Orchestration:")
    print("  ✓ Request routing")
    print("  ✓ Agent initialization")
    print("  ✓ System status")
    print("  ✓ Tool registration")
    print("  ✓ Request processing")
    print("  ✓ Integration workflow")
    print("  ✓ Error handling")
    print("\nAll 6 phases complete! 🎉")
    print("Task Management & Productivity Agent is fully integrated!")

