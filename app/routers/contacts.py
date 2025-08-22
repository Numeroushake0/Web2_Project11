from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.contact import ContactCreate, ContactUpdate, ContactOut
from app.crud import contact as crud_contact
from app.deps import get_db, get_current_user
from app.models.user import User

router = APIRouter(prefix="/contacts", tags=["contacts"])

@router.post("/", response_model=ContactOut, status_code=201)
def create_contact(
    contact: ContactCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud_contact.create_contact(db, contact, user_id=current_user.id)

@router.get("/", response_model=List[ContactOut])
def list_contacts(
    skip: int = 0,
    limit: int = 100,
    query: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if query:
        return crud_contact.search_contacts(db, query, user_id=current_user.id)
    return crud_contact.get_contacts(db, skip, limit, user_id=current_user.id)

@router.get("/upcoming_birthdays", response_model=List[ContactOut])
def upcoming_birthdays(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud_contact.get_upcoming_birthdays(db, user_id=current_user.id)

@router.get("/{contact_id}", response_model=ContactOut)
def get_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_contact = crud_contact.get_contact(db, contact_id, user_id=current_user.id)
    if not db_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@router.put("/{contact_id}", response_model=ContactOut)
def update_contact(
    contact_id: int,
    contact: ContactUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_contact = crud_contact.update_contact(db, contact_id, contact, user_id=current_user.id)
    if not db_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@router.delete("/{contact_id}", status_code=204)
def delete_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    success = crud_contact.delete_contact(db, contact_id, user_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Contact not found")
