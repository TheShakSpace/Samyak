"""Data layer: Firebase (Firestore) and task/hours repositories."""
from db.firebase import get_firestore, get_task_manager, get_hours_repository, FirestoreTaskManager, HoursRepository
from db.factory import get_task_manager_factory

__all__ = [
    "get_firestore",
    "get_task_manager",
    "get_hours_repository",
    "get_task_manager_factory",
    "FirestoreTaskManager",
    "HoursRepository",
]
