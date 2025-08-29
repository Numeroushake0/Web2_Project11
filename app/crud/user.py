from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_by_email(db: Session, email: str):
    """
    Retrieve a user by their email address.

    Args:
        db (Session): Database session.
        email (str): Email address of the user.

    Returns:
        User | None: User object if found, else None.
    """
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserCreate):
    """
    Create a new user with hashed password.

    Args:
        db (Session): Database session.
        user (UserCreate): Data for the new user.

    Returns:
        User: Newly created user object.
    """
    hashed_password = pwd_context.hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def verify_password(plain_password, hashed_password):
    """
    Verify that a plain password matches the hashed password.

    Args:
        plain_password (str): Password provided by the user.
        hashed_password (str): Stored hashed password.

    Returns:
        bool: True if password matches, else False.
    """
    return pwd_context.verify(plain_password, hashed_password)
