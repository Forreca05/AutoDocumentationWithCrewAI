import uuid
from datetime import datetime
from typing import List, Optional

class Task:
    def __init__(self, title: str, priority: str = "média"):
        self.id = str(uuid.uuid4())
        self.title = title
        self.priority = priority.lower()
        self.completed = False
        self.created_at = datetime.now()
        self.completed_at: Optional[datetime] = None

    def mark_complete(self):
        if not self.completed:
            self.completed = True
            self.completed_at = datetime.now()

    def __repr__(self):
        status = "✓" if self.completed else "✗"
        return f"[{status}] {self.title} ({self.priority})"


class TaskManager:
    VALID_PRIORITIES = ["baixa", "média", "alta"]

    def __init__(self):
        self.tasks: List[Task] = []

    def add_task(self, title: str, priority: str = "média") -> Task:
        if priority.lower() not in self.VALID_PRIORITIES:
            raise ValueError(f"Prioridade inválida. Use uma das: {self.VALID_PRIORITIES}")
        task = Task(title, priority)
        self.tasks.append(task)
        return task

    def get_pending_tasks(self, sorted_by_priority: bool = True) -> List[Task]:
        pending = [t for t in self.tasks if not t.completed]
        if sorted_by_priority:
            priority_order = {p: i for i, p in enumerate(["alta", "média", "baixa"])}
            pending.sort(key=lambda t: (priority_order[t.priority], t.created_at))
        return pending

    def complete_task(self, task_id: str) -> bool:
        for task in self.tasks:
            if task.id == task_id and not task.completed:
                task.mark_complete()
                return True
        return False

    def get_completed_tasks(self) -> List[Task]:
        return [t for t in self.tasks if t.completed]

    def list_all_tasks(self) -> List[Task]:
        return self.tasks
