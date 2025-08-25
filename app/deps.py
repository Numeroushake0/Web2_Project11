from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from app.db.database import SessionLocal
from app.models.user import User
from app.crud import user as crud_user
from app.core.config import settings
from app.services.cache import get_cache, set_cache

import asyncio

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception


    cached_email = await get_cache(f"user:{user_id}")
    if cached_email:
        db_user = db.query(User).filter(User.email == cached_email.decode()).first()
        if db_user:
            return db_user

    db_user = crud_user.get_user_by_id(db, user_id)
    if db_user is None:
        raise credentials_exception

    await set_cache(f"user:{user_id}", db_user.email, expire=600)

    return db_user
