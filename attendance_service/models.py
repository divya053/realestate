from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from datetime import datetime

class Attendance(Base):
    __tablename__ = "attendances"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    status = Column(String)  # 'in' or 'out'
