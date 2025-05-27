from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    mobile: str
    password: str

class UserUpdate(BaseModel):
    email: str = None
    mobile: str = None

class UserOut(BaseModel):
    id: int
    email: str
    mobile: str
    is_verified: bool

    class Config:
        orm_mode = True
