from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date


class ContactBase(BaseModel):
    """
    Base schema for contact data.

    Attributes:
        first_name (str): First name of the contact.
        last_name (str): Last name of the contact.
        email (EmailStr): Email address of the contact.
        phone (str): Phone number of the contact.
        birthday (date): Birthday of the contact.
        additional_info (Optional[str]): Optional additional information about the contact.
    """
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    birthday: date
    additional_info: Optional[str] = None


class ContactCreate(ContactBase):
    """Schema for creating a new contact."""
    pass


class ContactUpdate(BaseModel):
    """
    Schema for updating an existing contact.

    All fields are optional to allow partial updates.
    """
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    birthday: Optional[date] = None
    additional_info: Optional[str] = None


class ContactOut(ContactBase):
    """
    Schema for returning contact data.

    Attributes:
        id (int): Unique identifier of the contact.
    """
    id: int

    class Config:
        orm_mode = True