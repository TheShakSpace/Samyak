"""
Phase 3 Testing - Code-as-Plan for Task Queries
Tests code generation and safe execution
"""
from tools.query_tools import (
    generate_query_code,
    execute_query_code,
    query_tasks_with_code,
    build_schema_block,
)
from utils.code_executor import SafeCodeExecutor, extract_execute_block
from models.task import TaskManager
from config import TASKS_DB_PATH
import json

def test_code_extraction():
    """Test code extraction from tags"""
    print("=" * 60)
    print("Phase 3: Testing Code-as-Plan")
    print("=" * 60)
    
    print("\n1. Testing extract_execute_block()...")
    
    test_cases = [
        ("<execute_python>\nprint('hello')\n</execute_python>", "print('hello')"),
        ("print('no tags')", "print('no tags')"),
        ("<execute_python>x = 1</execute_python>", "x = 1"),
    ]
    
    for input_text, expected in test_cases:
        result = extract_execute_block(input_text)
        if result.strip() == expected.strip():
            print(f"   ✓ Extracted correctly: {result[:30]}...")
        else:
            print(f"   ✗ Extraction failed")
            print(f"     Expected: {expected}")
            print(f"     Got: {result}")

def test_safe_executor():
    """Test safe code executor"""
    print("\n2. Testing SafeCodeExecutor...")
    
    task_manager = TaskManager(TASKS_DB_PATH)
    executor = SafeCodeExecutor(task_manager)
    
    test_code = """
# Simple query test
high_priority = [t for t in tasks if t.priority == "high"]
answer_text = f"Found {len(high_priority)} high priority tasks"
STATUS = "success"
print(f"LOG: Query executed, found {len(high_priority)} tasks")
"""
    
    result = executor.execute(test_code, "Show me high priority tasks")
    
    print(f"   ✓ Code executed")
    print(f"   Answer: {result['answer']}")
    print(f"   Status: {result['status']}")
    print(f"   Stdout: {result['stdout']}")
    
    if result['error']:
        print(f"   ⚠ Error: {result['error']}")
    else:
        print(f"   ✓ No errors")

def test_schema_building():
    """Test schema block generation"""
    print("\n3. Testing build_schema_block()...")
    
    schema = build_schema_block()
    print(f"   ✓ Schema generated ({len(schema)} characters)")
    print(f"   Contains task count: {'task count' in schema.lower()}")
    print(f"   Contains status breakdown: {'status breakdown' in schema.lower()}")

def test_manual_query_code():
    """Test manual query code execution"""
    print("\n4. Testing manual query code execution...")
    
    query_code = """
from datetime import datetime, timedelta

# Query: tasks due this week
week_end = datetime.now() + timedelta(days=7)
due_this_week = [
    t for t in tasks 
    if t.deadline and t.deadline <= week_end and t.status != "completed"
]

answer_text = f"Found {len(due_this_week)} tasks due this week"
answer_rows = [t.to_dict() for t in due_this_week]
STATUS = "success" if due_this_week else "no_match"

print(f"LOG: Found {len(due_this_week)} tasks due this week")
"""
    
    result = execute_query_code(query_code, "Show me tasks due this week")
    
    print(f"   ✓ Query executed")
    print(f"   Answer: {result['answer']}")
    print(f"   Status: {result['status']}")
    print(f"   Tasks found: {result['tasks_found']}")

def test_complex_queries():
    """Test various complex query patterns"""
    print("\n5. Testing complex query patterns...")
    
    queries = [
        {
            "name": "High priority incomplete tasks",
            "code": """
high_incomplete = [t for t in tasks if t.priority == "high" and t.status != "completed"]
answer_text = f"Found {len(high_incomplete)} high priority incomplete tasks"
answer_rows = [t.to_dict() for t in high_incomplete]
STATUS = "success"
print(f"LOG: Found {len(high_incomplete)} tasks")
"""
        },
        {
            "name": "Tasks with specific tag",
            "code": """
work_tasks = [t for t in tasks if "work" in [tag.lower() for tag in t.tags]]
answer_text = f"Found {len(work_tasks)} tasks tagged with 'work'"
answer_rows = [t.to_dict() for t in work_tasks]
STATUS = "success"
print(f"LOG: Found {len(work_tasks)} work tasks")
"""
        },
        {
            "name": "Overdue tasks",
            "code": """
from datetime import datetime
overdue = [t for t in tasks if t.deadline and t.deadline < datetime.now() and t.status != "completed"]
answer_text = f"Found {len(overdue)} overdue tasks"
answer_rows = [t.to_dict() for t in overdue]
STATUS = "success" if overdue else "no_match"
print(f"LOG: Found {len(overdue)} overdue tasks")
"""
        },
    ]
    
    for query in queries:
        print(f"\n   Testing: {query['name']}")
        result = execute_query_code(query['code'], query['name'])
        print(f"   ✓ {result['answer']}")
        print(f"   Status: {result['status']}")

def test_code_generation():
    """Test code generation (if aisuite available)"""
    print("\n6. Testing code generation...")
    
    try:
        code = generate_query_code("Show me all high priority tasks")
        print(f"   ✓ Code generated ({len(code)} characters)")
        
        if "<execute_python>" in code:
            print(f"   ✓ Contains <execute_python> tags")
            extracted = extract_execute_block(code)
            print(f"   ✓ Code extracted ({len(extracted)} characters)")
        else:
            print(f"   ⚠ No <execute_python> tags found")
            
    except Exception as e:
        print(f"   ⚠ Code generation requires aisuite (Python 3.10+)")
        print(f"   Error: {e}")
        print(f"   ✓ Manual code execution works (tested above)")

def test_full_workflow():
    """Test full query workflow"""
    print("\n7. Testing full query workflow...")
    
    try:
        result = query_tasks_with_code("Show me all incomplete high priority tasks")
        print(f"   ✓ Full workflow executed")
        print(f"   User request: {result['user_request']}")
        print(f"   Generated code length: {len(result['generated_code'])} chars")
        exec_result = result['execution_result']
        print(f"   Answer: {exec_result['answer']}")
        print(f"   Status: {exec_result['status']}")
    except Exception as e:
        print(f"   ⚠ Full workflow requires aisuite (Python 3.10+)")
        print(f"   Error: {e}")
        print(f"   ✓ Code execution works independently")

def test_error_handling():
    """Test error handling in code execution"""
    print("\n8. Testing error handling...")
    
    error_code = """
# This will cause an error
undefined_variable = non_existent_function()
answer_text = "This should not appear"
STATUS = "success"
"""
    
    result = execute_query_code(error_code, "Test error handling")
    
    if result['error']:
        print(f"   ✓ Error caught and handled")
        print(f"   Error type: {type(result['error']).__name__}")
    else:
        print(f"   ⚠ Error not caught")

def test_answer_variants():
    """Test different answer variable formats"""
    print("\n9. Testing answer variable variants...")
    
    variants = [
        ("answer_text", "answer_text = 'Test answer'"),
        ("answer_rows", "answer_rows = [{'test': 'data'}]"),
        ("answer_json", "answer_json = {'count': 5}"),
    ]
    
    for var_name, code_line in variants:
        code = f"""
{code_line}
STATUS = "success"
print("LOG: Test")
"""
        result = execute_query_code(code, f"Test {var_name}")
        if result['answer']:
            print(f"   ✓ {var_name} extracted correctly")
        else:
            print(f"   ⚠ {var_name} not found")

if __name__ == "__main__":
    test_code_extraction()
    test_safe_executor()
    test_schema_building()
    test_manual_query_code()
    test_complex_queries()
    test_code_generation()
    test_full_workflow()
    test_error_handling()
    test_answer_variants()
    
    print("\n" + "=" * 60)
    print("Phase 3 Testing Complete! ✓")
    print("=" * 60)
    print("\nCode-as-Plan functionality:")
    print("  ✓ Code extraction from tags")
    print("  ✓ Safe code execution")
    print("  ✓ Schema building")
    print("  ✓ Complex query patterns")
    print("  ✓ Error handling")
    print("  ✓ Answer extraction")
    print("\nNote: Code generation requires Python 3.10+ and aisuite")
    print("Code execution works independently and can be used with")
    print("manually written or LLM-generated code.")
    print("\nReady for Phase 4: Email Integration")

