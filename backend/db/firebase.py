"""Firebase Firestore client and repositories (backend only)."""
import os
from datetime import datetime
from typing import Optional, List
from config import USE_FIREBASE, GOOGLE_APPLICATION_CREDENTIALS, FIREBASE_PROJECT_ID

_db = None


def get_firestore():
    """Initialize and return Firestore client. Uses GOOGLE_APPLICATION_CREDENTIALS."""
    global _db
    if _db is not None:
        return _db
    if not USE_FIREBASE or not GOOGLE_APPLICATION_CREDENTIALS:
        return None
    try:
        import firebase_admin
        from firebase_admin import credentials, firestore
    except ImportError:
        return None
    cred_path = GOOGLE_APPLICATION_CREDENTIALS
    if not os.path.isabs(cred_path):
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        cred_path = os.path.join(base, cred_path)
    if not os.path.exists(cred_path):
        return None
    try:
        if not firebase_admin._apps:
            opts = {"credential": credentials.Certificate(cred_path)}
            if FIREBASE_PROJECT_ID:
                opts["project_id"] = FIREBASE_PROJECT_ID
            firebase_admin.initialize_app(opts)
        _db = firestore.client()
        return _db
    except Exception:
        return None


class FirestoreTaskManager:
    """TaskManager interface backed by Firestore (same API as models.task.TaskManager)."""
    COLLECTION = "tasks"

    def __init__(self):
        self._db = get_firestore()
        if self._db is None:
            raise RuntimeError("Firestore not available. Set USE_FIREBASE and GOOGLE_APPLICATION_CREDENTIALS.")

    def _coll(self):
        return self._db.collection(self.COLLECTION)

    def add_task(self, task) -> "Task":
        from models.task import Task
        ref = self._coll().document(task.task_id)
        ref.set(task.to_dict())
        return task

    def get_task(self, task_id: str) -> Optional["Task"]:
        from models.task import Task
        doc = self._coll().document(task_id).get()
        if not doc.exists:
            return None
        return Task.from_dict(doc.to_dict())

    def get_all_tasks(self) -> List["Task"]:
        from models.task import Task
        docs = self._coll().stream()
        return [Task.from_dict(doc.to_dict()) for doc in docs]

    def update_task(self, task_id: str, **kwargs) -> Optional["Task"]:
        task = self.get_task(task_id)
        if not task:
            return None
        for key, value in kwargs.items():
            if hasattr(task, key):
                setattr(task, key, value)
        task.updated_at = datetime.now()
        self._coll().document(task_id).set(task.to_dict())
        return task

    def delete_task(self, task_id: str) -> bool:
        ref = self._coll().document(task_id)
        if not ref.get().exists:
            return False
        ref.delete()
        return True


class HoursRepository:
    """Working hours (time log) repository in Firestore."""
    COLLECTION = "working_hours"

    def __init__(self):
        self._db = get_firestore()
        if self._db is None:
            raise RuntimeError("Firestore not available. Set USE_FIREBASE and GOOGLE_APPLICATION_CREDENTIALS.")

    def _coll(self):
        return self._db.collection(self.COLLECTION)

    def add(self, wh) -> "WorkingHours":
        from models.working_hours import WorkingHours
        self._coll().document(wh.id).set(wh.to_dict())
        return wh

    def get_by_id(self, id: str) -> Optional["WorkingHours"]:
        from models.working_hours import WorkingHours
        doc = self._coll().document(id).get()
        if not doc.exists:
            return None
        return WorkingHours.from_dict(doc.to_dict())

    def list_by_task(self, task_id: str) -> List["WorkingHours"]:
        from models.working_hours import WorkingHours
        docs = self._coll().where("task_id", "==", task_id).stream()
        return [WorkingHours.from_dict(d.to_dict()) for d in docs]

    def list_by_user(self, user_id: str, from_date=None, to_date=None) -> List["WorkingHours"]:
        from models.working_hours import WorkingHours
        q = self._coll().where("user_id", "==", user_id)
        if from_date:
            q = q.where("date", ">=", from_date.isoformat() if hasattr(from_date, "isoformat") else str(from_date))
        if to_date:
            q = q.where("date", "<=", to_date.isoformat() if hasattr(to_date, "isoformat") else str(to_date))
        docs = q.stream()
        return [WorkingHours.from_dict(d.to_dict()) for d in docs]

    def list_by_date_range(self, from_date, to_date, task_id: Optional[str] = None, user_id: Optional[str] = None) -> List["WorkingHours"]:
        from models.working_hours import WorkingHours
        q = self._coll().where("date", ">=", from_date.isoformat() if hasattr(from_date, "isoformat") else str(from_date)).where("date", "<=", to_date.isoformat() if hasattr(to_date, "isoformat") else str(to_date))
        if task_id:
            q = q.where("task_id", "==", task_id)
        if user_id:
            q = q.where("user_id", "==", user_id)
        docs = q.stream()
        return [WorkingHours.from_dict(d.to_dict()) for d in docs]


def get_task_manager():
    """Return Firestore-backed TaskManager. Use get_task_manager_factory() for JSON/Firestore switch."""
    return FirestoreTaskManager()


def get_hours_repository() -> Optional[HoursRepository]:
    if get_firestore() is None:
        return None
    try:
        return HoursRepository()
    except Exception:
        return None
