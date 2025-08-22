from fastapi import FastAPI
from app.routers import contacts
from app.db.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Contacts API")

app.include_router(contacts.router)

@app.get("/")
def read_root():
    return {"message": "Server is running!"}
