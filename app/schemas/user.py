from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    """
    Schema for creating a new user.

    Attributes:
        email (EmailStr): Email address of the user.
        password (str): Plain-text password for account creation.
    """
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    """
    Schema for user login.

    Attributes:
        email (EmailStr): Email address of the user.
        password (str): Password for authentication.
    """
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """
    Schema for returning user data.

    Attributes:
        id (int): Unique identifier of the user.
        email (EmailStr): Email address of the user.
        is_verified (bool): Whether the user's email is verified.
        avatar_url (Optional[str]): Optional URL of the user's avatar.
    """
    id: int
    email: EmailStr
    is_verified: bool
    avatar_url: Optional[str] = None

    class Config:
        from_attributes = True


class Token(BaseModel):
    """
    Schema for JWT tokens.

    Attributes:
        access_token (str): Access token for authentication.
        refresh_token (str): Refresh token for renewing access.
        token_type (str): Type of the token, default is 'bearer'.
    """
    access_token: str
    refresh_token: str
    token_type: str = "bearer"