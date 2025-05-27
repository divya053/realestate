from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from datetime import datetime

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    assigned_to = Column(String)
    role = Column(String)
    status = Column(String)  # 'pending', 'completed', 'overdue'
    deadline = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
