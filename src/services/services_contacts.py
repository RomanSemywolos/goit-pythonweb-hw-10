from sqlalchemy.ext.asyncio import AsyncSession

from schemas.schemas_contact import NewContact, EditContact
from repo.repo_contacts import ContactRepo

class ContactManager:
    def __init__(self, session: AsyncSession):
        self.contact_repo = ContactRepo(session)

    async def fetch_contacts(self, offset: int, max_results: int):
        return await self.contact_repo.fetch_all_contacts(offset, max_results)

    async def fetch_contact(self, contact_id: int):
        return await self.contact_repo.fetch_contact_by_id(contact_id)

    async def add_contact(self, contact_data: NewContact):
        return await self.contact_repo.create_contact(contact_data)

    async def modify_contact(self, contact_id: int, update_data: EditContact):
        return await self.contact_repo.update_contact(contact_id, update_data)

    async def delete_contact(self, contact_id: int):
        return await self.contact_repo.remove_contact(contact_id)

    async def search_for_contacts(self, query: str, offset: int, max_results: int):
        return await self.contact_repo.search_for_contacts(query, offset, max_results)

    async def retrieve_upcoming_birthdays(self):
        return await self.contact_repo.fetch_upcoming_birthdays()
