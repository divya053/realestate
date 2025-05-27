from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from auth_service.models import User, OTP, Base
from auth_service.schemas import UserCreate, Token, OTPRequest, OTPVerify, Role
from auth_service.utils import hash_password, verify_password, create_access_token
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import random

router = APIRouter()

# Database
SQLALCHEMY_DATABASE_URL = 'sqlite:///./auth.db'
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post('/register', status_code=201)
def register(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(400, 'Email already registered')
    hashed = hash_password(user.password)
    db_user = User(email=user.email, password_hash=hashed)
    db.add(db_user)
    db.commit()
    return {'message': 'User registered'}

@router.post('/send-otp')
def send_otp(req: OTPRequest, db: Session = Depends(get_db)):
    code = f"{random.randint(100000, 999999)}"
    db_otp = OTP(email=req.email, code=code)
    db.add(db_otp)
    db.commit()
    # Simulate email
    print(f"Sent OTP {code} to {req.email}")
    return {'message': 'OTP sent'}

@router.post('/verify-otp')
def verify_otp(req: OTPVerify, db: Session = Depends(get_db)):
    record = db.query(OTP).filter(OTP.email == req.email, OTP.code == req.code).first()
    if not record:
        raise HTTPException(400, 'Invalid OTP')
    return {'message': 'OTP verified'}

@router.post('/login', response_model=Token)
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials')
    token = create_access_token({'sub': db_user.email, 'role': db_user.role})
    return {'access_token': token}

# Role-based dependency
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/login')

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get('sub')
        role: str = payload.get('role')
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate credentials')
    return {'email': email, 'role': role}


def require_roles(roles: list[str]):
    def dependency(current: dict = Depends(get_current_user)):
        if current['role'] not in roles:
            raise HTTPException(status_code=403, detail='Forbidden')
        return current
    return dependency

@router.get('/admin-only', dependencies=[Depends(require_roles([Role.ADMIN]))])
def admin_endpoint():
    return {'message': 'Admin access granted'}