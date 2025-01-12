from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Contact
from app.schemas import ContactCreate, ContactResponse
from app.database import get_db
from app.auth import get_current_user
from typing import List

router = APIRouter(prefix="/contacts", tags=["contacts"])

@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(
    contact: ContactCreate, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)
):
    new_contact = Contact(**contact.dict(), owner_id=current_user.id)
    db.add(new_contact)
    await db.commit()
    return new_contact

@router.get("/", response_model=List[ContactResponse])
async def get_contacts(db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    result = await db.execute(select(Contact).filter(Contact.owner_id == current_user.id))
    return result.scalars().all()

@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(contact_id: int, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    result = await db.execute(select(Contact).filter(Contact.id == contact_id, Contact.owner_id == current_user.id))
    contact = result.scalars().first()
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact
