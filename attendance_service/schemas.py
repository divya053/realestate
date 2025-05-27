from pydantic import BaseModel
from datetime import datetime

class AttendanceCreate(BaseModel):
    user_id: int
    status: str  # 'in' or 'out'

class AttendanceOut(BaseModel):
    id: int
    user_id: int
    timestamp: datetime
    status: str

    class Config:
        orm_mode = True
