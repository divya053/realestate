from fastapi import FastAPI, Depends
from schemas import UserCreate, UserUpdate, UserOut
from crud import create_user, update_user
from database import SessionLocal, engine, Base
from models import User
Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/register", response_model=UserOut)
def register(user: UserCreate, db=Depends(get_db)):
    return create_user(db, user)

@app.put("/profile/{user_id}", response_model=UserOut)
def update_profile(user_id: int, user: UserUpdate, db=Depends(get_db)):
    return update_user(db, user_id, user)

@app.post("/verify/{user_id}")
def verify(user_id: int, db=Depends(get_db)):
    user = db.query(User).get(user_id)
    user.is_verified = True
    db.commit()
    return {"status": "verified"}
