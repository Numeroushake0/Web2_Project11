from sqlalchemy import Column, Integer, String, Date
from app.db.database import Base


class Contact(Base):
    """
    Contact model representing a user's contact.

    Attributes:
        id (int): Primary key.
        first_name (str): First name of the contact.
        last_name (str): Last name of the contact.
        email (str): Unique email address of the contact.
        phone (str): Unique phone number of the contact.
        birthday (date): Birthday of the contact.
        additional_info (str | None): Optional additional information about the contact.
    """

    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, unique=True, index=True, nullable=False)
    birthday = Column(Date, nullable=False)
    additional_info = Column(String, nullable=True)
