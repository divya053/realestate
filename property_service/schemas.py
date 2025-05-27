from pydantic import BaseModel
from enum import Enum

class PropertyStatus(str, Enum):
    draft = "Draft"
    submitted = "Submitted"
    verified = "Verified"
    listed = "Listed"
    deal = "Deal"
    closed = "Closed"

class PropertyCreate(BaseModel):
    title: str
    type: str

class PropertyUpdate(BaseModel):
    title: str = None
    type: str = None
    status: PropertyStatus = None

class PropertyOut(BaseModel):
    id: int
    title: str
    type: str
    status: PropertyStatus

    class Config:
        orm_mode = True
