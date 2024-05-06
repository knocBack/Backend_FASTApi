from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from enum import Enum

class UserRole(str, Enum):
    admin = "admin"
    customer = "customer"

class UserSortFields(str, Enum):
    id = "id"
    name = "name"
    email = "email"
    role = "role"

class UserPayload(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: UserRole

    class Config:
        from_attributes = True

class UserSignup(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: UserRole

class UserUpdate(BaseModel):
    name: str
    email: EmailStr
    role: UserRole
    password: str

    class Config:
        form_attributes = True
