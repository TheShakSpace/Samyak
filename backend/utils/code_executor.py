import re
import io
import sys
import traceback
from typing import Dict, Any, Optional
from datetime import datetime
from models.task import TaskManager, Task
from config import TASKS_DB_PATH

def extract_execute_block(text: str) -> str:
    """
    Extract Python code from <execute_python>...</execute_python> tags.
    If no tags found, assumes the text is already raw Python code.
    """
    if not text:
        raise ValueError("Empty content passed to code executor")
    
    match = re.search(r"<execute_python>(.*?)</execute_python>", text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return text.strip()


class SafeCodeExecutor:
    """
    Safe code executor for running generated Python code in a controlled environment.
    Provides access to TaskManager and task data while preventing dangerous operations.
    """
    
    def __init__(self, task_manager: Optional[TaskManager] = None):
        self.task_manager = task_manager or TaskManager(TASKS_DB_PATH)
        self.allowed_modules = {
            'datetime', 'json', 're', 'math', 'statistics', 'collections'
        }
    
    def _create_safe_globals(self, user_request: Optional[str] = None) -> Dict[str, Any]:
        """Create safe global namespace for code execution"""
        from datetime import datetime, timedelta
        import json
        import re
        import math
        import statistics
        from collections import Counter, defaultdict
        
        return {
            'datetime': datetime,
            'timedelta': timedelta,
            'json': json,
            're': re,
            'math': math,
            'statistics': statistics,
            'Counter': Counter,
            'defaultdict': defaultdict,
            'user_request': user_request or '',
            'TaskManager': TaskManager,
            'Task': Task,
        }
    
    def _create_safe_locals(self) -> Dict[str, Any]:
        """Create safe local namespace with task data"""
        all_tasks = self.task_manager.get_all_tasks()
        
        return {
            'task_manager': self.task_manager,
            'tasks': all_tasks,
            'all_tasks': all_tasks,
        }
    
    def execute(
        self,
        code_or_content: str,
        user_request: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Execute Python code safely in a controlled environment.
        
        Args:
            code_or_content: Python code or content with <execute_python> tags
            user_request: Original user request for context
        
        Returns:
            Dictionary with execution results, stdout, errors, and extracted answers
        """
        code = extract_execute_block(code_or_content)
        
        safe_globals = self._create_safe_globals(user_request)
        safe_locals = self._create_safe_locals()
        
        stdout_buf = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = stdout_buf
        
        error_text = None
        try:
            exec(code, safe_globals, safe_locals)
        except Exception as e:
            error_text = traceback.format_exc()
        finally:
            sys.stdout = old_stdout
        
        printed = stdout_buf.getvalue().strip()
        
        answer = (
            safe_locals.get("answer_text") or
            safe_locals.get("answer_rows") or
            safe_locals.get("answer_json") or
            safe_locals.get("result")
        )
        
        status = safe_locals.get("STATUS", "unknown")
        
        return {
            "code": code,
            "stdout": printed,
            "error": error_text,
            "answer": answer,
            "status": status,
            "tasks_after": self.task_manager.get_all_tasks(),
        }

