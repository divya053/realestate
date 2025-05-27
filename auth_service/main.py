
from fastapi import FastAPI
from auth_service.routes import router
from auth_service.models import Base
from auth_service.routes import engine
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

# Ensure DB and tables are created
Base.metadata.create_all(bind=engine)
