"""Tools for logging and querying working hours (productivity tracking)."""
import uuid
from datetime import datetime
from typing import Optional, Dict

from db.factory import get_task_manager_factory
from db.firebase import get_hours_repository
from models.working_hours import WorkingHours


def log_working_hours(
    task_id: str,
    user_id: str,
    minutes: int,
    date: Optional[str] = None,
    notes: str = "",
) -> Dict:
    """
    Log working hours for a task.
    Args:
        task_id: Task ID
        user_id: User email or uid
        minutes: Minutes spent
        date: Date (YYYY-MM-DD or ISO) or None for today
        notes: Optional notes
    Returns:
        Dict with status and logged entry
    """
    task_manager = get_task_manager_factory()
    task = task_manager.get_task(task_id)
    if not task:
        return {"status": "error", "message": f"Task {task_id} not found"}
    repo = get_hours_repository()
    if repo is None:
        return {"status": "error", "message": "Working hours not available (Firebase required)"}
    date_val = datetime.now().date()
    if date:
        try:
            if "T" in date:
                date_val = datetime.fromisoformat(date.replace("Z", "+00:00")).date()
            else:
                date_val = datetime.strptime(date[:10], "%Y-%m-%d").date()
        except Exception:
            pass
    wh = WorkingHours(
        id=f"WH{uuid.uuid4().hex[:8].upper()}",
        task_id=task_id,
        user_id=user_id,
        minutes=minutes,
        date=date_val,
        notes=notes,
    )
    repo.add(wh)
    return {
        "status": "success",
        "message": f"Logged {minutes} min for task {task_id}",
        "working_hours": wh.to_dict(),
    }


def get_working_hours(
    task_id: Optional[str] = None,
    user_id: Optional[str] = None,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
) -> Dict:
    """
    Get working hours with optional filters.
    Args:
        task_id: Filter by task
        user_id: Filter by user
        from_date: Start date (YYYY-MM-DD)
        to_date: End date (YYYY-MM-DD)
    Returns:
        Dict with list of working_hours
    """
    repo = get_hours_repository()
    if repo is None:
        return {"status": "error", "message": "Working hours not available", "entries": []}
    from_d = to_d = None
    if from_date:
        try:
            from_d = datetime.strptime(from_date[:10], "%Y-%m-%d").date()
        except Exception:
            pass
    if to_date:
        try:
            to_d = datetime.strptime(to_date[:10], "%Y-%m-%d").date()
        except Exception:
            pass
    if from_d and to_d:
        entries = repo.list_by_date_range(from_d, to_d, task_id=task_id, user_id=user_id)
    elif task_id:
        entries = repo.list_by_task(task_id)
    elif user_id:
        entries = repo.list_by_user(user_id, from_date=from_d, to_date=to_d)
    else:
        entries = []
        if from_d and to_d:
            entries = repo.list_by_date_range(from_d, to_d)
    return {
        "status": "success",
        "count": len(entries),
        "entries": [e.to_dict() for e in entries],
    }
