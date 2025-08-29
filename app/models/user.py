from sqlalchemy import Column, Integer, String, Boolean
from app.db.database import Base


class User(Base):
    """
    User model representing an application user.

    Attributes:
        id (int): Primary key.
        email (str): Unique email address of the user.
        hashed_password (str): Hashed password for authentication.
        is_verified (bool): Indicates if the user has verified their email.
        avatar_url (str | None): Optional URL of the user's avatar image.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    avatar_url = Column(String, nullable=True)
