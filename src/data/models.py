from datetime import datetime
from typing import List

from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    Boolean,
    Text,
    ForeignKey,
    func
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import DateTime

# Base Class for ORM Models
class ORMBase(DeclarativeBase):
    pass

# Contact Model
class ContactModel(ORMBase):
    __tablename__ = "contacts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    birth_date: Mapped[Date] = mapped_column(Date, nullable=False)
    extra_info: Mapped[str] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column('created_at', DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column('updated_at', DateTime, default=func.now(), onupdate=func.now())
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    owner: Mapped["UserModel"] = relationship("UserModel", back_populates="contacts")

# User Model
class UserModel(ORMBase):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    avatar: Mapped[str] = mapped_column(String(255), nullable=True)
    confirmed: Mapped[bool] = mapped_column(Boolean, default=False)
    contacts: Mapped["List[ContactModel]"] = relationship("ContactModel", back_populates="owner")

