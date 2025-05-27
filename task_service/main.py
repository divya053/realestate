from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import models, schemas, crud

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/tasks/", response_model=schemas.TaskOut)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db, task)

@app.patch("/tasks/{task_id}", response_model=schemas.TaskOut)
def update_task(task_id: int, task_update: schemas.TaskUpdate, db: Session = Depends(get_db)):
    task = crud.update_task_status(db, task_id, task_update.status)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.get("/tasks/", response_model=list[schemas.TaskOut])
def get_tasks(role: str = None, db: Session = Depends(get_db)):
    return crud.get_tasks(db, role)

@app.post("/tasks/escalate/")
def escalate_tasks(db: Session = Depends(get_db)):
    tasks = crud.escalate_overdue_tasks(db)
    return {"message": f"Escalated {len(tasks)} tasks."}
