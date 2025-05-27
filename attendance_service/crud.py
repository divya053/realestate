from sqlalchemy.orm import Session
from models import Attendance
from schemas import AttendanceCreate
from datetime import datetime

def get_last_attendance(db: Session, user_id: int):
    return db.query(Attendance).filter(Attendance.user_id == user_id).order_by(Attendance.timestamp.desc()).first()

def create_attendance(db: Session, attendance: AttendanceCreate):
    last = get_last_attendance(db, attendance.user_id)
    if attendance.status == 'out':
        if not last or last.status != 'in':
            raise ValueError("Cannot mark 'out' before 'in'")
    elif attendance.status == 'in':
        if last and last.status == 'in':
            raise ValueError("Already marked 'in'")
    db_attendance = Attendance(user_id=attendance.user_id, status=attendance.status, timestamp=datetime.utcnow())
    db.add(db_attendance)
    db.commit()
    db.refresh(db_attendance)
    return db_attendance

def get_attendance_by_user_and_date(db: Session, user_id: int, date: datetime):
    return db.query(Attendance).filter(
        Attendance.user_id == user_id,
        Attendance.timestamp.between(date, date.replace(hour=23, minute=59, second=59))
    ).all()
