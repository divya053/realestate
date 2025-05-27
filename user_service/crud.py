from models import User
from sqlalchemy.orm import Session

def create_user(db: Session, user_data):
    user = User(**user_data.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def update_user(db: Session, user_id: int, updates):
    user = db.query(User).get(user_id)
    for key, value in updates.dict(exclude_unset=True).items():
        setattr(user, key, value)
    db.commit()
    return user
