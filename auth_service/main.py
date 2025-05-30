
from fastapi import FastAPI
from routes import router
from models import Base
from routes import engine
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
app.include_router(router, prefix="/auth")

Base.metadata.create_all(bind=engine)
