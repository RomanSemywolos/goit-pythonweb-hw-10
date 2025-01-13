from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict


# Base Schema for Contact
class ContactSchemaBase(BaseModel):
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    email: EmailStr
    phone: str = Field(max_length=20)
    birth_date: date
    extra_info: Optional[str] = Field(default=None, max_length=500)


# Schema for Contact Creation
class NewContact(ContactSchemaBase):
    pass


# Schema for Contact Update
class EditContact(ContactSchemaBase):
    given_name: Optional[str] = Field(default=None, max_length=50)
    family_name: Optional[str] = Field(default=None, max_length=50)
    email_address: Optional[EmailStr] = None
    phone_number: Optional[str] = Field(default=None, max_length=20)
    dob: Optional[date] = None
    extra_info: Optional[str] = Field(default=None, max_length=500)


# Schema for Contact Response
class ContactSchemaResponse(ContactSchemaBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
