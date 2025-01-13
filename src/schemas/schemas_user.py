# Imports
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional


# Schema for Creating a User
class NewUserSchema(BaseModel):
    user_name: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=6)


# Schema for User Response
class UserSchemaResponse(BaseModel):
    id: int
    user_name: str
    email: str
    avatar: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


# Schema for User Login
class LoginSchema(BaseModel):
    email: EmailStr
    password: str


# Schema for Tokens
class AuthTokenSchema(BaseModel):
    token_access: str
    token_refresh: str
    token_type: str = "bearer"
