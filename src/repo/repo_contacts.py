from datetime import date, timedelta
from typing import List, Optional

from sqlalchemy import select, or_, and_, extract
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.models import ContactModel
from schemas.schemas_contact import NewContact, EditContact


# Repository Class for Contact Operations
class ContactRepo:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def fetch_all_contacts(self, offset: int = 0, max_limit: int = 100, user_ref: int = None) -> List[ContactModel]:
        query = select(ContactModel).filter_by(user_id=user_ref).offset(offset).limit(max_limit)
        result = await self.db_session.execute(query)
        return result.scalars().all()

    async def fetch_contact_by_id(self, contact_ref: int, user_ref: int) -> Optional[ContactModel]:
        query = select(ContactModel).filter_by(id=contact_ref, user_id=user_ref)
        result = await self.db_session.execute(query)
        return result.scalar_one_or_none()

    async def create_contact(self, data: NewContact, user_ref: int) -> ContactModel:
        contact_info = data.model_dump()
        contact_info['user_id'] = user_ref
        new_contact = ContactModel(**contact_info)
        self.db_session.add(new_contact)
        await self.db_session.commit()
        await self.db_session.refresh(new_contact)
        return new_contact

    async def update_contact(self, contact_ref: int, data: EditContact, user_ref: int) -> Optional[ContactModel]:
        query = select(ContactModel).filter_by(id=contact_ref, user_id=user_ref)
        result = await self.db_session.execute(query)
        contact_to_update = result.scalar_one_or_none()

        if contact_to_update:
            for field, value in data.model_dump(exclude_unset=True).items():
                setattr(contact_to_update, field, value)
            await self.db_session.commit()
            await self.db_session.refresh(contact_to_update)

        return contact_to_update

    async def remove_contact(self, contact_ref: int, user_ref: int) -> Optional[ContactModel]:
        query = select(ContactModel).filter_by(id=contact_ref, user_id=user_ref)
        result = await self.db_session.execute(query)
        contact_to_remove = result.scalar_one_or_none()

        if contact_to_remove:
            await self.db_session.delete(contact_to_remove)
            await self.db_session.commit()

        return contact_to_remove

    async def search_for_contacts(
        self, search_term: str, offset: int = 0, max_limit: int = 10, user_ref: int = None
    ) -> List[ContactModel]:
        search_pattern = f"%{search_term}%"
        query = select(ContactModel).filter(
            and_(
                or_(
                    ContactModel.first_name.ilike(search_pattern),
                    ContactModel.last_name.ilike(search_pattern),
                    ContactModel.contact_email.ilike(search_pattern)
                ),
                ContactModel.user_id == user_ref
            )
        ).offset(offset).limit(max_limit)

        result = await self.db_session.execute(query)
        return result.scalars().all()

    async def fetch_upcoming_birthdays(self, user_ref: int) -> List[ContactModel]:
        current_date = date.today()
        end_date = current_date + timedelta(days=7)

        query = select(ContactModel).filter(
            and_(
                or_(
                    and_(
                        extract('month', ContactModel.birthdate) == current_date.month,
                        extract('day', ContactModel.birthdate) >= current_date.day,
                        extract('day', ContactModel.birthdate) <= end_date.day
                    ),
                    and_(
                        extract('month', ContactModel.birthdate) == end_date.month,
                        extract('day', ContactModel.birthdate) <= end_date.day
                    )
                ),
                ContactModel.user_id == user_ref
            )
        )
        result = await self.db_session.execute(query)
        return result.scalars().all()
