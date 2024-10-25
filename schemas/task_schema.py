# app/schemas/task_schema.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Schema for creating a task (without id, date_time, and created_by)
class TaskCreate(BaseModel):
    name: str
    status: str  # 'TODO', 'InProgress', 'Completed'

# Schema for updating a task (now with optional date_time)
class TaskUpdate(BaseModel):
    id: int
    name: str
    status: str
    date_time: Optional[datetime] = None  # Make it optional for updates    

# Schema for reading task details (response)
class TaskRead(BaseModel):
    id: int
    name: str
    status: str
    date_time: datetime
    creator: Optional[str]  # This will hold the email of the user

    class Config:
        orm_mode = True
