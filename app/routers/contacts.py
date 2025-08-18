from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.contact import ContactCreate, ContactUpdate, ContactOut
from app.crud import contact as crud_contact
from app.deps import get_db

router = APIRouter(prefix="/contacts", tags=["contacts"])

@router.post("/", response_model=ContactOut)
def create_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    return crud_contact.create_contact(db, contact)

@router.get("/", response_model=List[ContactOut])
def list_contacts(skip: int = 0, limit: int = 100, query: str = None, db: Session = Depends(get_db)):
    if query:
        return crud_contact.search_contacts(db, query)
    return crud_contact.get_contacts(db, skip, limit)

@router.get("/upcoming_birthdays", response_model=List[ContactOut])
def upcoming_birthdays(db: Session = Depends(get_db)):
    return crud_contact.get_upcoming_birthdays(db)

@router.get("/{contact_id}", response_model=ContactOut)
def get_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = crud_contact.get_contact(db, contact_id)
    if not db_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@router.put("/{contact_id}", response_model=ContactOut)
def update_contact(contact_id: int, contact: ContactUpdate, db: Session = Depends(get_db)):
    db_contact = crud_contact.update_contact(db, contact_id, contact)
    if not db_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@router.d
