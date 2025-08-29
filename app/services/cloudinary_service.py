import cloudinary
import cloudinary.uploader
from app.core.config import settings

cloudinary.config(
    cloud_name=settings.cloudinary_name,
    api_key=settings.cloudinary_api_key,
    api_secret=settings.cloudinary_api_secret
)


def upload_avatar(file):
    """
    Upload an avatar image to Cloudinary.

    Args:
        file: File object to upload.

    Returns:
        str: Secure URL of the uploaded avatar.
    """
    result = cloudinary.uploader.upload(file, folder="avatars")
    return result["secure_url"]
