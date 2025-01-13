from typing import List, Optional

from fastapi import APIRouter, HTTPException, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from data.database import fetch_db_session
from src.data.models import UserModel
from schemas.schemas_contact import NewContact, EditContact, ContactSchemaResponse as CSResponse
from services.services_contacts import ContactManager
from api.api_auth import fetch_user

contact_router = APIRouter(prefix="/contacts", tags=["contacts"])

# Fetch Contacts
@contact_router.get("/", response_model=List[CSResponse])
async def get_all_contacts(
    offset: int = 0,
    max_results: int = 100,
    query: Optional[str] = Query(None, description="Search by name, last name or email"),
    db: AsyncSession = Depends(fetch_db_session),
    active_user: UserModel = Depends(fetch_user)
):
    service = ContactManager(db)
    if query:
        result = await service.search_for_contacts(query, offset, max_results, active_user.id)
    else:
        result = await service.fetch_contacts(offset, max_results, active_user.id)
    return result

# Fetch Upcoming Birthdays
@contact_router.get("/birthdays/", response_model=List[CSResponse])
async def get_birthdays(
    db: AsyncSession = Depends(fetch_db_session),
    active_user: UserModel = Depends(fetch_user)
):
    service = ContactManager(db)
    birthday_list = await service.retrieve_upcoming_birthdays(active_user.id)
    return birthday_list

# Fetch Single Contact
@contact_router.get("/{contact_id}", response_model=CSResponse)
async def get_single_contact(
    contact_id: int,
    db: AsyncSession = Depends(fetch_db_session),
    active_user: UserModel = Depends(fetch_user)
):
    service = ContactManager(db)
    single_contact = await service.fetch_contact(contact_id, active_user.id)
    if single_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return single_contact

# Create New Contact
@contact_router.post("/", response_model=CSResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(
    data: NewContact,
    db: AsyncSession = Depends(fetch_db_session),
    active_user: UserModel = Depends(fetch_user)
):
    service = ContactManager(db)
    return await service.add_contact(data, active_user.id)

# Update Existing Contact
@contact_router.put("/{contact_id}", response_model=CSResponse)
async def update_contact(
    contact_id: int,
    updates: EditContact,
    db: AsyncSession = Depends(fetch_db_session),
    active_user: UserModel = Depends(fetch_user)
):
    service = ContactManager(db)
    updated_contact = await service.modify_contact(contact_id, updates, active_user.id)
    if updated_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return updated_contact

# Delete Contact
@contact_router.delete("/{contact_id}", response_model=CSResponse)
async def delete_contact(
    contact_id: int,
    db: AsyncSession = Depends(fetch_db_session),
    active_user: UserModel = Depends(fetch_user)
):
    service = ContactManager(db)
    deleted_contact = await service.delete_contact(contact_id, active_user.id)
    if deleted_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return deleted_contact
