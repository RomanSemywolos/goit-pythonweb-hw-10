import cloudinary
import cloudinary.uploader
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.config import config
from data.database import fetch_db_session
from src.data.models import UserModel
from schemas.schemas_user import UserSchemaResponse as UResponse, NewUserSchema as UCreate, AuthTokenSchema as TSchema, LoginSchema as ULogin
from services.services_auth import (
    generate_access_token as generate_token,
    hash_password as hash_pwd,
    verify_user_credentials as verify_user,
    create_email_verification_token as email_verify_token
)
from repo.repo_users import UserRepo

# Cloudinary Configuration
cloudinary.config(
    cloud_name=config.CLOUDINARY_CLOUD_NAME,
    api_key=config.CLOUDINARY_API_KEY,
    api_secret=config.CLOUDINARY_API_SECRET
)

# Router Setup
router = APIRouter(prefix="/auth", tags=["auth"])
token_dependency = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

# Fetch current user
async def fetch_user(token: str = Depends(token_dependency), db: AsyncSession = Depends(fetch_db_session)):
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, config.JWT_SECRET_KEY, algorithms=[config.JWT_ALGORITHM])
        user_email = payload.get("sub")
        if user_email is None:
            raise credentials_error
    except JWTError:
        raise credentials_error

    user_repo_instance = UserRepo(db)
    db_user = await user_repo_instance.fetch_user_by_email(user_email)
    if db_user is None:
        raise credentials_error
    return db_user

# Register New User
@router.post("/register", response_model=UResponse, status_code=status.HTTP_201_CREATED)
async def add_user(user_data: UCreate, db: AsyncSession = Depends(fetch_db_session)):
    repo_instance = UserRepo(db)

    existing = await repo_instance.fetch_user_by_email(user_data.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists"
        )

    secure_password = hash_pwd(user_data.password)
    new_user = await repo_instance.add_user(user_data, secure_password)

    return UResponse(
        id=new_user.id,
        username=new_user.user_name,
        email=new_user.email
    )

# Login User
@router.post("/login", response_model=TSchema)
async def user_login(
        login_data: OAuth2PasswordRequestForm = Depends(),
        db: AsyncSession = Depends(fetch_db_session)
):
    verified_user = await verify_user(login_data.user_name, login_data.password, db)
    if not verified_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = generate_token(
        data={"sub": verified_user.email},
        expires_delta=config.ACCESS_TOKEN_LIFETIME
    )

    refresh = generate_token(
        data={"sub": verified_user.email},
        expires_delta=config.REFRESH_TOKEN_LIFETIME
    )

    return {
        "access_token": token,
        "refresh_token": refresh,
        "token_type": "bearer"
    }

# Upload Avatar
@router.post("/upload-avatar", response_model=UResponse)
async def avatar_upload(
        uploaded_file: UploadFile = File(...),
        active_user: UserModel = Depends(fetch_user),
        db: AsyncSession = Depends(fetch_db_session)
):
    upload_result = cloudinary.uploader.upload(uploaded_file.file, folder="avatars")
    active_user.avatar = upload_result['secure_url']
    await db.commit()

    return UResponse(
        id=active_user.id,
        username=active_user.user_name,
        email=active_user.email,
        avatar=active_user.avatar
    )

# Get Current User Info
@router.get("/me", response_model=UResponse)
async def get_profile(active_user: UserModel = Depends(fetch_user)):
    return UResponse(
        id=active_user.id,
        username=active_user.user_name,
        email=active_user.email,
        avatar=active_user.avatar
    )
