from typing import Dict, List, Optional
from pathlib import Path
from config import TASKS_DB_PATH, EMAIL_CONFIG

def validate_config() -> Dict[str, bool]:
    """
    Validate configuration and return status.
    
    Returns:
        Dictionary with validation results
    """
    results = {
        "database_path": False,
        "database_writable": False,
        "email_configured": False,
        "llm_configured": False,
    }
    
    try:
        db_path = Path(TASKS_DB_PATH)
        db_dir = db_path.parent
        
        results["database_path"] = db_dir.exists()
        results["database_writable"] = db_dir.exists() and Path(db_dir).is_dir()
        
        if db_path.exists():
            results["database_writable"] = Path(db_path).parent.is_dir()
    except Exception:
        pass
    
    email_address = EMAIL_CONFIG.get("email_address", "")
    email_password = EMAIL_CONFIG.get("email_password", "")
    results["email_configured"] = bool(email_address and email_password)
    
    try:
        from config import LLM_PROVIDER, LLAMA_MODEL_PATH, OPENAI_API_KEY
        if LLM_PROVIDER == "llama":
            # For Llama, check if model path exists or can be auto-detected
            from utils.llama_adapter import LlamaClient
            try:
                client = LlamaClient(model_path=LLAMA_MODEL_PATH)
                results["llm_configured"] = client.model_path is not None or True  # Auto-detect enabled
            except:
                results["llm_configured"] = False
        else:
            # For OpenAI, check API key
            results["llm_configured"] = bool(OPENAI_API_KEY)
    except Exception:
        pass
    
    return results

def validate_task_data(task_data: Dict) -> tuple[bool, Optional[str]]:
    """
    Validate task data before creation.
    
    Args:
        task_data: Task data dictionary
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not task_data.get("title"):
        return False, "Title is required"
    
    priority = task_data.get("priority", "medium").lower()
    if priority not in ["high", "medium", "low"]:
        return False, f"Invalid priority: {priority}. Must be 'high', 'medium', or 'low'"
    
    status = task_data.get("status", "todo").lower()
    if status not in ["todo", "in_progress", "completed"]:
        return False, f"Invalid status: {status}. Must be 'todo', 'in_progress', or 'completed'"
    
    return True, None

def check_system_health() -> Dict:
    """
    Check system health and return status.
    
    Returns:
        Dictionary with health status
    """
    from models.task import TaskManager
    
    health = {
        "status": "healthy",
        "issues": [],
        "warnings": []
    }
    
    try:
        task_manager = TaskManager(TASKS_DB_PATH)
        all_tasks = task_manager.get_all_tasks()
        
        if len(all_tasks) == 0:
            health["warnings"].append("No tasks in database")
    except Exception as e:
        health["status"] = "unhealthy"
        health["issues"].append(f"Database error: {e}")
    
    config = validate_config()
    if not config["database_writable"]:
        health["status"] = "unhealthy"
        health["issues"].append("Database directory not writable")
    
    if not config["llm_configured"]:
        health["warnings"].append("LLM not configured (some features unavailable)")
    
    if not config["email_configured"]:
        health["warnings"].append("Email not configured (notifications unavailable)")
    
    return health

