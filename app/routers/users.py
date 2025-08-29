from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user import User
from app.schemas.user import UserResponse
from app.services.cloudinary_service import upload_avatar
from app.deps import get_current_user  # <-- правильний імпорт

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserResponse)
async def read_me(current_user: User = Depends(get_current_user)):
    """
    Retrieve the current authenticated user's information.
    """
    return current_user


@router.post("/avatar", response_model=UserResponse)
async def upload_user_avatar(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Upload or update the authenticated user's avatar.
    """
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Only JPEG or PNG allowed."
        )

    avatar_url = upload_avatar(file.file)
    current_user.avatar_url = avatar_url
    db.commit()
    db.refresh(current_user)
    return current_user
