from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas import UserCreate, UserOut
from models import User, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

router = APIRouter()

SQLALCHEMY_DATABASE_URL = "sqlite:///./userservice.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=UserOut)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = User(email=user.email, password=user.password, full_name=user.full_name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/profile", response_model=UserOut)
def get_profile():
    return {"email": "test@example.com", "full_name": "John Doe"}

