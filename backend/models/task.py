from datetime import datetime
from typing import Optional, List
import json
from pathlib import Path

class Task:
    def __init__(
        self,
        task_id: str,
        title: str,
        description: str = "",
        priority: str = "medium",
        deadline: Optional[datetime] = None,
        status: str = "todo",
        assignee: str = "me",
        tags: Optional[List[str]] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        completed_at: Optional[datetime] = None,
    ):
        self.task_id = task_id
        self.title = title
        self.description = description
        self.priority = priority
        self.deadline = deadline
        self.status = status
        self.assignee = assignee
        self.tags = tags or []
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
        self.completed_at = completed_at

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "deadline": self.deadline.isoformat() if self.deadline else None,
            "status": self.status,
            "assignee": self.assignee,
            "tags": self.tags,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }

    @classmethod
    def from_dict(cls, data: dict):
        task = cls(
            task_id=data["task_id"],
            title=data["title"],
            description=data.get("description", ""),
            priority=data.get("priority", "medium"),
            deadline=datetime.fromisoformat(data["deadline"]) if data.get("deadline") else None,
            status=data.get("status", "todo"),
            assignee=data.get("assignee", "me"),
            tags=data.get("tags", []),
        )
        if data.get("created_at"):
            task.created_at = datetime.fromisoformat(data["created_at"])
        if data.get("updated_at"):
            task.updated_at = datetime.fromisoformat(data["updated_at"])
        if data.get("completed_at"):
            task.completed_at = datetime.fromisoformat(data["completed_at"])
        return task


class TaskManager:
    def __init__(self, db_path: str = "data/tasks.json"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.tasks = self._load_tasks()

    def _load_tasks(self) -> List[Task]:
        if not self.db_path.exists():
            return []
        try:
            with open(self.db_path, "r") as f:
                data = json.load(f)
                return [Task.from_dict(task_data) for task_data in data]
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _save_tasks(self):
        with open(self.db_path, "w") as f:
            json.dump([task.to_dict() for task in self.tasks], f, indent=2)

    def add_task(self, task: Task):
        self.tasks.append(task)
        self._save_tasks()
        return task

    def get_task(self, task_id: str) -> Optional[Task]:
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        return None

    def get_all_tasks(self) -> List[Task]:
        return self.tasks

    def update_task(self, task_id: str, **kwargs) -> Optional[Task]:
        task = self.get_task(task_id)
        if not task:
            return None
        for key, value in kwargs.items():
            if hasattr(task, key):
                setattr(task, key, value)
        task.updated_at = datetime.now()
        self._save_tasks()
        return task

    def delete_task(self, task_id: str) -> bool:
        task = self.get_task(task_id)
        if task:
            self.tasks.remove(task)
            self._save_tasks()
            return True
        return False

