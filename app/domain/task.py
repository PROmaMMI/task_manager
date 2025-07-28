from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"

@dataclass
class Task:
    id: int | None
    title: str
    description: str | None
    status: TaskStatus
    deadline: datetime | None
    created_at: datetime
    updated_at: datetime
    user_id: int