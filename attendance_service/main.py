from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import models, schemas, crud
from datetime import datetime

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/attendance/", response_model=schemas.AttendanceOut)
def mark_attendance(attendance: schemas.AttendanceCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_attendance(db, attendance)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/attendance/{user_id}/{date}", response_model=list[schemas.AttendanceOut])
def get_attendance(user_id: int, date: str, db: Session = Depends(get_db)):
    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")
    return crud.get_attendance_by_user_and_date(db, user_id, date_obj)
