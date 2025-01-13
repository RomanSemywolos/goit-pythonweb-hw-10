from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.models import UserModel
from schemas.schemas_user import NewUserSchema


# Repository Class for User Operations
class UserRepo:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def add_user(self, user_data: NewUserSchema, hashed_pass: str) -> UserModel:
        new_user = UserModel(
            user_name=user_data.user_name,
            email=user_data.email,
            password=hashed_pass
        )
        self.db_session.add(new_user)
        await self.db_session.commit()
        await self.db_session.refresh(new_user)
        return new_user

    async def fetch_user_by_email(self, email: str) -> Optional[UserModel]:
        query = select(UserModel).filter_by(email=email)
        result = await self.db_session.execute(query)
        return result.scalar_one_or_none()
