import random
import time
from fastapi import APIRouter, HTTPException, Depends, status, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import User
from app.schemas import UserCreate, UserResponse, Token, EmailVerification
from app.database import get_db
from app.auth import create_access_token, verify_password, get_password_hash, get_current_user
from app.email_utils import send_email
import cloudinary.uploader

router = APIRouter(prefix="/users", tags=["users"])

VERIFICATION_EXPIRATION = 300  # 5 хвилин
verification_codes = {}

def add_verification_code(email, code):
    verification_codes[email] = {"code": code, "timestamp": time.time()}

def is_code_valid(email, code):
    entry = verification_codes.get(email)
    if not entry or time.time() - entry["timestamp"] > VERIFICATION_EXPIRATION:
        return False
    return entry["code"] == code

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).filter(User.email == user.email))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")

    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username, email=user.email, hashed_password=hashed_password, is_verified=False)
    db.add(new_user)
    await db.commit()

    # для надсилання email
    code = random.randint(100000, 999999)
    add_verification_code(user.email, code)
    send_email(
        to_email=user.email,
        subject="Verify your email",
        body=f"Your verification code is: {code}"
    )
    return new_user

@router.post("/verify-email")
async def verify_email(data: EmailVerification, db: AsyncSession = Depends(get_db)):
    if not is_code_valid(data.email, int(data.code)):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired verification code")

    result = await db.execute(select(User).filter(User.email == data.email))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user.is_verified = True
    db.add(user)
    await db.commit()
    verification_codes.pop(data.email, None)  # Видалення
    return {"message": "Email verified successfully"}

@router.post("/avatar")
async def update_avatar(
    file: UploadFile, current_user=Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    result = cloudinary.uploader.upload(file.file, folder="avatars")
    current_user.avatar_url = result["url"]
    db.add(current_user)
    await db.commit()
    return {"avatar_url": current_user.avatar_url}
