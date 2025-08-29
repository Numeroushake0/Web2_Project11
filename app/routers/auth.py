from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from passlib.context import CryptContext

from app.deps import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.services.email import send_email
from app.services.cache import set_cache
from app.core.config import settings
from app.crud import user as crud_user

router = APIRouter(prefix="/auth", tags=["auth"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=15)) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def create_refresh_token(data: dict, expires_delta: timedelta = timedelta(days=7)) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    existing_user = crud_user.get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = pwd_context.hash(user_data.password)
    new_user = crud_user.create_user(db, user_data.email, hashed_password)

    token = create_access_token({"sub": new_user.email}, expires_delta=timedelta(hours=24))
    verify_link = f"{settings.frontend_url}/verify/{token}"
    background_tasks.add_task(send_email, email=new_user.email, subject="Verify your email",
                              body=f"<a href='{verify_link}'>Click to verify your email</a>")
    return new_user

@router.get("/verify/{token}")
async def verify_email(token: str, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid token")

    user = crud_user.get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_verified = True
    db.commit()
    return {"message": "Email successfully verified"}

@router.post("/login", response_model=Token)
async def login(form_data: UserLogin, db: Session = Depends(get_db)):
    user = crud_user.get_user_by_email(db, form_data.email)
    if not user or not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not user.is_verified:
        raise HTTPException(status_code=403, detail="Email not verified")

    access_token = create_access_token({"sub": user.email})
    refresh_token = create_refresh_token({"sub": user.email})
    await set_cache(f"user:{user.id}", user.email, expire=600)
    return Token(access_token=access_token, refresh_token=refresh_token)

@router.post("/forgot-password")
async def forgot_password(email: str, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    user = crud_user.get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    token = create_access_token({"sub": user.email}, expires_delta=timedelta(hours=1))
    reset_link = f"{settings.frontend_url}/reset-password/{token}"
    background_tasks.add_task(send_email, email=user.email, subject="Reset your password",
                              body=f"<a href='{reset_link}'>Click to reset password</a>")
    return {"message": "Password reset link sent to your email"}

@router.post("/reset-password/{token}")
async def reset_password(token: str, new_password: str, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid token")

    user = crud_user.get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.hashed_password = pwd_context.hash(new_password)
    db.commit()
    return {"message": "Password successfully reset"}
