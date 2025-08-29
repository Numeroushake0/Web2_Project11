from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from fastapi_limiter.depends import RateLimiter

from app.schemas.contact import ContactCreate, ContactUpdate, ContactOut
from app.crud import contact as crud_contact
from app.deps import get_db, get_current_user
from app.models.user import User

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.post(
    "/", 
    response_model=ContactOut, 
    status_code=201,
    dependencies=[Depends(RateLimiter(times=5, seconds=60))]
)
def create_contact(
    contact: ContactCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new contact for the current user.

    Args:
        contact (ContactCreate): Contact data.
        db (Session): Database session.
        current_user (User): Authenticated user.

    Returns:
        ContactOut: Created contact.
    """
    return crud_contact.create_contact(db, contact, user_id=current_user.id)


@router.get("/", response_model=List[ContactOut])
def list_contacts(
    skip: int = 0,
    limit: int = 100,
    query: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    List contacts for the current user, with optional search and pagination.

    Args:
        skip (int): Number of records to skip.
        limit (int): Maximum number of records to return.
        query (str, optional): Search query string.
        db (Session): Database session.
        current_user (User): Authenticated user.

    Returns:
        List[ContactOut]: List of contacts.
    """
    if query:
        return crud_contact.search_contacts(db, query, user_id=current_user.id)
    return crud_contact.get_contacts(db, skip, limit, user_id=current_user.id)


@router.get("/upcoming_birthdays", response_model=List[ContactOut])
def upcoming_birthdays(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve contacts with birthdays in the upcoming week for the current user.

    Args:
        db (Session): Database session.
        current_user (User): Authenticated user.

    Returns:
        List[ContactOut]: List of contacts with upcoming birthdays.
    """
    return crud_contact.get_upcoming_birthdays(db, user_id=current_user.id)


@router.get("/{contact_id}", response_model=ContactOut)
def get_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve a contact by ID for the current user.

    Args:
        contact_id (int): Contact ID.
        db (Session): Database session.
        current_user (User): Authenticated user.

    Raises:
        HTTPException: 404 if contact not found.

    Returns:
        ContactOut: Contact data.
    """
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
    """
    Update an existing contact for the current user.

    Args:
        contact_id (int): Contact ID.
        contact (ContactUpdate): Updated contact data.
        db (Session): Database session.
        current_user (User): Authenticated user.

    Raises:
        HTTPException: 404 if contact not found.

    Returns:
        ContactOut: Updated contact.
    """
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
    """
    Delete a contact by ID for the current user.

    Args:
        contact_id (int): Contact ID.
        db (Session): Database session.
        current_user (User): Authenticated user.

    Raises:
        HTTPException: 404 if contact not found.
    """
    success = crud_contact.delete_contact(db, contact_id, user_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Contact not found")
