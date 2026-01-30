"""Working hours (time log) model for productivity tracking."""
from datetime import datetime
from typing import Optional


class WorkingHours:
    def __init__(
        self,
        id: str,
        task_id: str,
        user_id: str,
        minutes: int,
        date: Optional[datetime] = None,
        notes: str = "",
        created_at: Optional[datetime] = None,
    ):
        self.id = id
        self.task_id = task_id
        self.user_id = user_id
        self.minutes = minutes
        self.date = date or datetime.now().date()
        if isinstance(self.date, datetime):
            self.date = self.date.date()
        self.notes = notes or ""
        self.created_at = created_at or datetime.now()

    def to_dict(self):
        return {
            "id": self.id,
            "task_id": self.task_id,
            "user_id": self.user_id,
            "minutes": self.minutes,
            "date": self.date.isoformat() if hasattr(self.date, "isoformat") else str(self.date),
            "notes": self.notes,
            "created_at": self.created_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "WorkingHours":
        date_val = data.get("date")
        if isinstance(date_val, str):
            date_val = datetime.fromisoformat(date_val.replace("Z", "+00:00")).date() if "T" in date_val else datetime.strptime(date_val, "%Y-%m-%d").date()
        created = data.get("created_at")
        if isinstance(created, str):
            created = datetime.fromisoformat(created.replace("Z", "+00:00"))
        return cls(
            id=data["id"],
            task_id=data["task_id"],
            user_id=data["user_id"],
            minutes=int(data["minutes"]),
            date=date_val,
            notes=data.get("notes", ""),
            created_at=created,
        )
