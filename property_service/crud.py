from models import Property
from sqlalchemy.orm import Session

def create_property(db: Session, prop_data):
    prop = Property(**prop_data.dict())
    db.add(prop)
    db.commit()
    db.refresh(prop)
    return prop

def update_property(db: Session, prop_id, updates):
    prop = db.query(Property).get(prop_id)
    for key, value in updates.dict(exclude_unset=True).items():
        setattr(prop, key, value)
    db.commit()
    return prop
