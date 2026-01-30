from typing import Dict, Optional
from models.task import TaskManager, Task
from config import TASKS_DB_PATH, LLM_MODEL
from utils.code_executor import SafeCodeExecutor, extract_execute_block
import json
from datetime import datetime

task_manager = TaskManager(TASKS_DB_PATH)
executor = SafeCodeExecutor(task_manager)

QUERY_PROMPT_TEMPLATE = """You are a task management assistant. Generate Python code to query and analyze tasks.

Task Schema:
- task_id: str (unique identifier)
- title: str
- description: str
- priority: str ("high", "medium", "low")
- deadline: datetime or None
- status: str ("todo", "in_progress", "completed")
- assignee: str
- tags: List[str]
- created_at: datetime
- updated_at: datetime
- completed_at: datetime or None

Available in execution environment:
- task_manager: TaskManager instance
- tasks: List[Task] (all tasks)
- all_tasks: List[Task] (same as tasks)
- datetime, timedelta: for date operations
- json, re, math, statistics: standard libraries

REQUIREMENTS:
1. Parse the user request to understand what they want
2. Write Python code to query/analyze tasks
3. Set a variable `answer_text` with a human-readable response (1-2 sentences)
4. Optionally set `answer_rows` (list of task dicts) or `answer_json` (structured data)
5. Set `STATUS` to "success", "no_match", or "error"
6. Print a brief log message to stdout

OUTPUT FORMAT:
Wrap your code in <execute_python> tags:
<execute_python>
# Your Python code here
# Example:
from datetime import datetime, timedelta

# Parse user request
user_query = user_request.lower()

# Query tasks
if "high priority" in user_query:
    filtered = [t for t in tasks if t.priority == "high"]
elif "due this week" in user_query:
    week_end = datetime.now() + timedelta(days=7)
    filtered = [t for t in tasks if t.deadline and t.deadline <= week_end]
else:
    filtered = tasks

# Set answer
answer_text = f"Found {len(filtered)} tasks matching your criteria."
answer_rows = [t.to_dict() for t in filtered]
STATUS = "success"

print(f"LOG: Found {len(filtered)} tasks")
</execute_python>

User request: {user_request}
"""

def build_schema_block() -> str:
    """Build a schema description from current tasks"""
    all_tasks = task_manager.get_all_tasks()
    
    if not all_tasks:
        return "No tasks in database yet."
    
    sample_task = all_tasks[0]
    schema = f"""
Task Schema:
{json.dumps(sample_task.to_dict(), indent=2, default=str)}

Current task count: {len(all_tasks)}
Status breakdown: {{
    "todo": {len([t for t in all_tasks if t.status == 'todo'])},
    "in_progress": {len([t for t in all_tasks if t.status == 'in_progress'])},
    "completed": {len([t for t in all_tasks if t.status == 'completed'])}
}}
Priority breakdown: {{
    "high": {len([t for t in all_tasks if t.priority == 'high'])},
    "medium": {len([t for t in all_tasks if t.priority == 'medium'])},
    "low": {len([t for t in all_tasks if t.priority == 'low'])}
}}
"""
    return schema


def generate_query_code(user_request: str, model: str = LLM_MODEL) -> str:
    """
    Generate Python code to answer a user's query using code-as-plan pattern.
    
    Args:
        user_request: Natural language query about tasks
        model: LLM model to use (default from config)
    
    Returns:
        Generated code wrapped in <execute_python> tags
    """
    try:
        import aisuite as ai
        client = ai.Client()
    except ImportError:
        return f"""<execute_python>
# Code generation requires aisuite (Python 3.10+)
# Manual query implementation:

answer_text = "Code generation requires Python 3.10+ and aisuite. Please use direct query tools instead."
STATUS = "error"
print("LOG: Code generation not available")
</execute_python>"""
    
    schema_block = build_schema_block()
    prompt = QUERY_PROMPT_TEMPLATE.format(user_request=user_request)
    full_prompt = f"{schema_block}\n\n{prompt}"
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You write safe, well-commented Python code to query and analyze task data."
                },
                {
                    "role": "user",
                    "content": full_prompt
                }
            ],
            temperature=0.2,
        )
        
        content = response.choices[0].message.content or ""
        return content
    except Exception as e:
        return f"""<execute_python>
# Error generating code: {e}
answer_text = "Unable to generate query code. Please try a simpler query."
STATUS = "error"
print(f"LOG: Code generation error: {e}")
</execute_python>"""


def execute_query_code(code: str, user_request: Optional[str] = None) -> Dict:
    """
    Execute generated query code safely.
    
    Args:
        code: Python code (with or without <execute_python> tags)
        user_request: Original user request for context
    
    Returns:
        Dictionary with execution results
    """
    result = executor.execute(code, user_request)
    
    return {
        "status": result["status"],
        "answer": result["answer"],
        "stdout": result["stdout"],
        "error": result["error"],
        "tasks_found": len(result.get("tasks_after", [])),
    }


def query_tasks_with_code(user_request: str, model: str = LLM_MODEL) -> Dict:
    """
    Query tasks using code-as-plan pattern.
    Generates code, executes it, and returns results.
    
    Args:
        user_request: Natural language query about tasks
        model: LLM model to use
    
    Returns:
        Dictionary with query results
    """
    code = generate_query_code(user_request, model)
    result = execute_query_code(code, user_request)
    
    return {
        "user_request": user_request,
        "generated_code": code,
        "execution_result": result,
    }

