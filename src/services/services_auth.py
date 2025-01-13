import secrets
from datetime import datetime, timedelta
from typing import Optional

from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.config import config
from repo.repo_users import UserRepo

# Initialize password context for hashing and verifying passwords
password_manager = CryptContext(schemes=["bcrypt"], deprecated="auto")


def generate_access_token(payload: dict, expiration_minutes: Optional[float] = None):
    token_data = payload.copy()
    if expiration_minutes:
        expiration_time = datetime.utcnow() + timedelta(minutes=expiration_minutes)
    else:
        expiration_time = datetime.utcnow() + timedelta(minutes=15)

    token_data.update({"exp": expiration_time})
    jwt_token = jwt.encode(token_data, config.JWT_SECRET_KEY, algorithm=config.JWT_ALGORITHM)
    return jwt_token


def validate_password(plain_text_password: str, encrypted_password: str) -> bool:
    return password_manager.verify(plain_text_password, encrypted_password)


def hash_password(password: str) -> str:
    return password_manager.hash(password)


async def verify_user_credentials(email: str, password: str, db_session: AsyncSession):
    user_repo = UserRepo(db_session)
    user_record = await user_repo.fetch_user_by_email(email)

    if not user_record:
        return False

    if not validate_password(password, user_record.password):
        return False

    return user_record


def create_email_verification_token() -> str:
    return secrets.token_urlsafe(32)
