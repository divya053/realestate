from sqlalchemy.orm import Session
from models import Task
from schemas import TaskCreate, TaskUpdate
from datetime import datetime

def create_task(db: Session, task: TaskCreate):
    db_task = Task(
        title=task.title,
        description=task.description,
        assigned_to=task.assigned_to,
        role=task.role,
        status='pending',
        deadline=task.deadline,
        created_at=datetime.utcnow()
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    print(f"Notification: Task '{db_task.title}' assigned to {db_task.assigned_to}")
    return db_task

def update_task_status(db: Session, task_id: int, status: str):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        task.status = status
        db.commit()
        db.refresh(task)
        return task
    return None

def get_tasks(db: Session, role: str = None):
    if role:
        return db.query(Task).filter(Task.role == role).all()
    return db.query(Task).all()

def escalate_overdue_tasks(db: Session):
    now = datetime.utcnow()
    tasks = db.query(Task).filter(Task.status == 'pending', Task.deadline < now).all()
    for task in tasks:
        task.status = 'overdue'
        print(f"Escalation: Task '{task.title}' is overdue!")
    db.commit()
    return tasks
