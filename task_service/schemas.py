from pydantic import BaseModel
from datetime import datetime

class TaskCreate(BaseModel):
    title: str
    description: str
    assigned_to: str
    role: str
    deadline: datetime

class TaskUpdate(BaseModel):
    status: str

class TaskOut(BaseModel):
    id: int
    title: str
    description: str
    assigned_to: str
    role: str
    status: str
    deadline: datetime
    created_at: datetime

    class Config:
        orm_mode = True
