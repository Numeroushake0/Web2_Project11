from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.routers import contacts, auth, users
from app.db.database import engine, Base
from app.core.config import settings
from fastapi_limiter import FastAPILimiter
import redis.asyncio as redis

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Contacts API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    redis_client = redis.from_url(f"redis://{settings.redis_host}:{settings.redis_port}")
    await FastAPILimiter.init(redis_client)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(contacts.router)

@app.get("/")
def read_root():
    return {"message": "Server is running!"}
