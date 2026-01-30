from typing import Dict, Optional, List
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from models.task import TaskManager, Task
from config import TASKS_DB_PATH, CHART_OUTPUT_DIR
from tools.task_tools import calculate_productivity_metrics
from utils.chart_reflection import reflect_on_chart
from utils.code_executor import extract_execute_block
import re

task_manager = TaskManager(TASKS_DB_PATH)
Path(CHART_OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

CHART_GENERATION_PROMPT = """You are a data visualization expert.

Generate Python code to create a productivity chart from task data.

Available data:
- tasks: List of Task objects with attributes: task_id, title, priority, status, deadline, created_at, completed_at, assignee, tags
- You can convert to DataFrame: df = pd.DataFrame([t.to_dict() for t in tasks])

User instruction: {instruction}

REQUIREMENTS:
1. Use matplotlib for plotting
2. Create clear, informative visualizations
3. Add title, axis labels, and legend if needed
4. Save the figure as '{output_path}' with dpi=300
5. Always call plt.close() at the end (no plt.show())
6. Include all necessary imports

OUTPUT FORMAT:
Wrap your code in <execute_python> tags:
<execute_python>
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

# Your visualization code here
# Example: df = pd.DataFrame([t.to_dict() for t in tasks])
# ... create chart ...
plt.savefig('{output_path}', dpi=300, bbox_inches='tight')
plt.close()
</execute_python>

Return ONLY the code wrapped in <execute_python> tags.
"""

def generate_chart_code(instruction: str, output_path: str, model: str = "openai:gpt-4o") -> str:
    """
    Generate Python code to create a chart from task data.
    
    Args:
        instruction: Natural language instruction for the chart
        output_path: Path where chart should be saved
        model: LLM model to use
    
    Returns:
        Generated code wrapped in <execute_python> tags
    """
    try:
        import aisuite as ai
        client = ai.Client()
    except ImportError:
        return f"""<execute_python>
# Chart generation requires aisuite (Python 3.10+)
import matplotlib.pyplot as plt
plt.figure(figsize=(10, 6))
plt.text(0.5, 0.5, 'Chart generation requires Python 3.10+', ha='center', va='center')
plt.title('Chart Generation Unavailable')
plt.savefig('{output_path}', dpi=300, bbox_inches='tight')
plt.close()
</execute_python>"""
    
    prompt = CHART_GENERATION_PROMPT.format(
        instruction=instruction,
        output_path=output_path
    )
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You write safe, well-commented matplotlib code to create data visualizations."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2,
        )
        
        content = response.choices[0].message.content or ""
        if "<execute_python>" not in content:
            content = f"<execute_python>\n{content}\n</execute_python>"
        return content
    except Exception as e:
        return f"""<execute_python>
# Error generating chart code: {e}
import matplotlib.pyplot as plt
plt.figure(figsize=(10, 6))
plt.text(0.5, 0.5, 'Chart generation error', ha='center', va='center')
plt.title('Error')
plt.savefig('{output_path}', dpi=300, bbox_inches='tight')
plt.close()
</execute_python>"""

def execute_chart_code(code: str, tasks: Optional[List[Task]] = None) -> Dict:
    """
    Execute chart generation code safely.
    
    Args:
        code: Python code (with or without <execute_python> tags)
        tasks: List of tasks to use in chart (if None, loads from TaskManager)
    
    Returns:
        Dictionary with execution results
    """
    if tasks is None:
        tasks = task_manager.get_all_tasks()
    
    code = extract_execute_block(code)
    
    safe_globals = {
        'plt': plt,
        'pd': pd,
        'datetime': datetime,
        'timedelta': timedelta,
        'tasks': tasks,
        'all_tasks': tasks,
    }
    
    safe_locals = {}
    
    try:
        exec(code, safe_globals, safe_locals)
        return {
            "status": "success",
            "message": "Chart generated successfully",
            "error": None
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Chart generation failed: {e}",
            "error": str(e)
        }

def create_productivity_chart(
    instruction: str,
    output_path: Optional[str] = None,
    model: str = "openai:gpt-4o",
    use_reflection: bool = True
) -> Dict:
    """
    Create a productivity chart with optional reflection.
    
    Args:
        instruction: Natural language instruction for the chart
        output_path: Path to save chart (default: data/charts/chart_v1.png)
        model: LLM model to use
        use_reflection: Whether to use reflection to improve the chart
    
    Returns:
        Dictionary with chart generation results
    """
    if output_path is None:
        output_path = f"{CHART_OUTPUT_DIR}/chart_v1.png"
    
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    code_v1 = generate_chart_code(instruction, output_path, model)
    result_v1 = execute_chart_code(code_v1)
    
    if result_v1["status"] != "success":
        return {
            "instruction": instruction,
            "version": "v1",
            "code": code_v1,
            "result": result_v1,
            "chart_path": None,
            "reflection": None,
        }
    
    if not use_reflection:
        return {
            "instruction": instruction,
            "version": "v1",
            "code": code_v1,
            "result": result_v1,
            "chart_path": output_path,
            "reflection": None,
        }
    
    output_path_v2 = output_path.replace("_v1", "_v2").replace(".png", "_v2.png")
    if "_v2" not in output_path_v2:
        output_path_v2 = output_path.replace(".png", "_v2.png")
    
    feedback, code_v2 = reflect_on_chart(
        chart_path=output_path,
        instruction=instruction,
        original_code=code_v1,
        model=model,
        output_path=output_path_v2
    )
    
    result_v2 = execute_chart_code(code_v2)
    
    return {
        "instruction": instruction,
        "version": "v2",
        "code_v1": code_v1,
        "code_v2": code_v2,
        "result_v1": result_v1,
        "result_v2": result_v2,
        "chart_path_v1": output_path,
        "chart_path_v2": output_path_v2 if result_v2["status"] == "success" else None,
        "reflection": {
            "feedback": feedback,
            "improved": result_v2["status"] == "success"
        }
    }

def create_task_completion_chart(days: int = 30, output_path: Optional[str] = None) -> Dict:
    """
    Create a chart showing task completion rate over time.
    
    Args:
        days: Number of days to analyze
        output_path: Path to save chart
    
    Returns:
        Dictionary with chart generation results
    """
    if output_path is None:
        output_path = f"{CHART_OUTPUT_DIR}/completion_rate.png"
    
    all_tasks = task_manager.get_all_tasks()
    cutoff_date = datetime.now() - timedelta(days=days)
    
    recent_tasks = [t for t in all_tasks if t.created_at >= cutoff_date]
    
    if not recent_tasks:
        return {
            "status": "error",
            "message": "No tasks found in the specified period",
            "chart_path": None
        }
    
    df = pd.DataFrame([t.to_dict() for t in recent_tasks])
    df['created_at'] = pd.to_datetime(df['created_at'])
    df['date'] = df['created_at'].dt.date
    
    daily_stats = df.groupby('date').agg({
        'task_id': 'count',
        'status': lambda x: (x == 'completed').sum()
    }).rename(columns={'task_id': 'total', 'status': 'completed'})
    daily_stats['completion_rate'] = (daily_stats['completed'] / daily_stats['total'] * 100).round(2)
    
    plt.figure(figsize=(12, 6))
    plt.plot(daily_stats.index, daily_stats['completion_rate'], marker='o', linewidth=2)
    plt.title(f'Task Completion Rate Over Last {days} Days', fontsize=14, fontweight='bold')
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Completion Rate (%)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return {
        "status": "success",
        "message": f"Chart created successfully",
        "chart_path": output_path,
        "data_points": len(daily_stats)
    }

def create_priority_distribution_chart(output_path: Optional[str] = None) -> Dict:
    """
    Create a chart showing task distribution by priority.
    
    Args:
        output_path: Path to save chart
    
    Returns:
        Dictionary with chart generation results
    """
    if output_path is None:
        output_path = f"{CHART_OUTPUT_DIR}/priority_distribution.png"
    
    all_tasks = task_manager.get_all_tasks()
    
    if not all_tasks:
        return {
            "status": "error",
            "message": "No tasks found",
            "chart_path": None
        }
    
    priority_counts = {'high': 0, 'medium': 0, 'low': 0}
    for task in all_tasks:
        priority = task.priority.lower()
        if priority in priority_counts:
            priority_counts[priority] += 1
    
    colors = ['#dc3545', '#ffc107', '#28a745']
    priorities = list(priority_counts.keys())
    counts = list(priority_counts.values())
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(priorities, counts, color=colors, alpha=0.7, edgecolor='black', linewidth=1.5)
    plt.title('Task Distribution by Priority', fontsize=14, fontweight='bold')
    plt.xlabel('Priority Level', fontsize=12)
    plt.ylabel('Number of Tasks', fontsize=12)
    plt.grid(True, alpha=0.3, axis='y')
    
    for bar, count in zip(bars, counts):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                str(count), ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return {
        "status": "success",
        "message": "Chart created successfully",
        "chart_path": output_path,
        "data": priority_counts
    }

