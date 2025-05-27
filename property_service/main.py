from fastapi import FastAPI, Depends
from schemas import PropertyCreate, PropertyUpdate, PropertyOut
from crud import create_property, update_property
from database import SessionLocal, engine, Base
from models import Property

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/properties", response_model=PropertyOut)
def create(prop: PropertyCreate, db=Depends(get_db)):
    return create_property(db, prop)

@app.put("/properties/{prop_id}", response_model=PropertyOut)
def update(prop_id: int, prop: PropertyUpdate, db=Depends(get_db)):
    return update_property(db, prop_id, prop)

@app.get("/properties/{prop_id}", response_model=PropertyOut)
def read(prop_id: int, db=Depends(get_db)):
    return db.query(Property).get(prop_id)
