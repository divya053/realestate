# property-service/routes.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from property_service.models import Property, Base
from property_service.schemas import PropertyCreate, PropertyOut
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

router = APIRouter()

SQLALCHEMY_DATABASE_URL = "sqlite:///./realestate_property.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/properties", response_model=PropertyOut)
def create_property(property: PropertyCreate, db: Session = Depends(get_db)):
    new_prop = Property(
        title=property.title,
        type=property.type,
        status=property.status
    )
    db.add(new_prop)
    db.commit()
    db.refresh(new_prop)
    return new_prop

@router.get("/properties/{property_id}", response_model=PropertyOut)
def get_property(property_id: int, db: Session = Depends(get_db)):
    prop = db.query(Property).filter(Property.id == property_id).first()
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
    return prop

@router.put("/properties/{property_id}", response_model=PropertyOut)
def update_property(property_id: int, property: PropertyCreate, db: Session = Depends(get_db)):
    prop = db.query(Property).filter(Property.id == property_id).first()
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
    prop.title = property.title
    prop.type = property.type
    prop.status = property.status
    db.commit()
    db.refresh(prop)
    return prop

@router.delete("/properties/{property_id}")
def delete_property(property_id: int, db: Session = Depends(get_db)):
    prop = db.query(Property).filter(Property.id == property_id).first()
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
    db.delete(prop)
    db.commit()
    return {"detail": "Property deleted"}
