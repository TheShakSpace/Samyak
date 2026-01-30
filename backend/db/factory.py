"""Factory: return JSON or Firestore TaskManager based on config."""
from config import USE_FIREBASE, TASKS_DB_PATH
from models.task import TaskManager


def get_task_manager_factory():
    """Return TaskManager: Firestore if USE_FIREBASE and credentials set, else JSON file."""
    if USE_FIREBASE:
        try:
            from db.firebase import FirestoreTaskManager
            return FirestoreTaskManager()
        except Exception:
            pass
    return TaskManager(TASKS_DB_PATH)
