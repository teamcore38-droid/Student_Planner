import uuid
from datetime import datetime

class Task:
    """
    Model Layer: Represents an individual academic task with strict type checking,
    module binding, and serialization helpers.
    """
    def __init__(
        self,
        title: str,
        module: str,
        due_date: str,
        priority: str,
        notes: str = "",
        completed: bool = False,
        username: str = "",
        task_id: str | None = None,
        created_at: str | None = None
    ):
        self.task_id = task_id if task_id else str(uuid.uuid4())
        self.username = username
        self.title = title.strip()
        self.module = module.strip()
        self.due_date = due_date.strip()
        self.priority = priority.strip()  # Enforce: "High", "Medium", "Low"
        self.notes = notes.strip()
        self.completed = completed
        self.created_at = created_at if created_at else datetime.now().isoformat()

    def to_dict(self) -> dict:
        """
        Serializes the Task object into a standard dictionary.
        
        Returns:
            dict: Representation of the task properties for JSON write.
        """
        return {
            "task_id": self.task_id,
            "username": self.username,
            "title": self.title,
            "module": self.module,
            "due_date": self.due_date,
            "priority": self.priority,
            "notes": self.notes,
            "completed": self.completed,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Task':
        """
        Creates a Task object from a serialized dictionary.
        
        Args:
            data (dict): Dict of task properties.
            
        Returns:
            Task: Reconstructed Task instance.
        """
        return cls(
            title=data.get("title", ""),
            module=data.get("module", ""),
            due_date=data.get("due_date", ""),
            priority=data.get("priority", "Medium"),
            notes=data.get("notes", ""),
            completed=data.get("completed", False),
            username=data.get("username", ""),
            task_id=data.get("task_id"),
            created_at=data.get("created_at")
        )
