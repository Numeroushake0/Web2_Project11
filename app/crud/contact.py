from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List
from app.models.contact import Contact
from app.schemas.contact import ContactCreate, ContactUpdate


def get_contact(db: Session, contact_id: int):
    """
    Retrieve a single contact by its ID.

    Args:
        db (Session): Database session.
        contact_id (int): ID of the contact to retrieve.

    Returns:
        Contact | None: Contact object if found, else None.
    """
    return db.query(Contact).filter(Contact.id == contact_id).first()


def get_contacts(db: Session, skip: int = 0, limit: int = 100):
    """
    Retrieve a list of contacts with optional pagination.

    Args:
        db (Session): Database session.
        skip (int): Number of records to skip.
        limit (int): Maximum number of records to return.

    Returns:
        List[Contact]: List of contact objects.
    """
    return db.query(Contact).offset(skip).limit(limit).all()


def search_contacts(db: Session, query: str):
    """
    Search contacts by first name, last name, or email.

    Args:
        db (Session): Database session.
        query (str): Search query string.

    Returns:
        List[Contact]: List of contacts matching the query.
    """
    return db.query(Contact).filter(
        (Contact.first_name.ilike(f"%{query}%")) |
        (Contact.last_name.ilike(f"%{query}%")) |
        (Contact.email.ilike(f"%{query}%"))
    ).all()


def get_upcoming_birthdays(db: Session, days: int = 7):
    """
    Retrieve contacts with birthdays in the next 'days' days.

    Args:
        db (Session): Database session.
        days (int): Number of upcoming days to check.

    Returns:
        List[Contact]: List of contacts with upcoming birthdays.
    """
    today = datetime.today().date()
    end_date = today + timedelta(days=days)
    return db.query(Contact).filter(
        Contact.birthday >= today,
        Contact.birthday <= end_date
    ).all()


def create_contact(db: Session, contact: ContactCreate):
    """
    Create a new contact in the database.

    Args:
        db (Session): Database session.
        contact (ContactCreate): Data for the new contact.

    Returns:
        Contact: Newly created contact object.
    """
    db_contact = Contact(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


def update_contact(db: Session, contact_id: int, contact: ContactUpdate):
    """
    Update an existing contact by ID.

    Args:
        db (Session): Database session.
        contact_id (int): ID of the contact to update.
        contact (ContactUpdate): Fields to update.

    Returns:
        Contact | None: Updated contact object if found, else None.
    """
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not db_contact:
        return None
    for key, value in contact.dict(exclude_unset=True).items():
        setattr(db_contact, key, value)
    db.commit()
    db.refresh(db_contact)
    return db_contact


def delete_contact(db: Session, contact_id: int):
    """
    Delete a contact by ID.

    Args:
        db (Session): Database session.
        contact_id (int): ID of the contact to delete.

    Returns:
        Contact | None: Deleted contact object if found, else None.
    """
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not db_contact:
        return None
    db.delete(db_contact)
    db.commit()
    return db_contact
