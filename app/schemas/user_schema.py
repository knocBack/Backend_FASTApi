from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from enum import Enum

# enum for different types of user roles
class UserRole(str, Enum):
    admin = "admin"
    customer = "customer"

# enum for different fields for user sort api
class UserSortFields(str, Enum):
    id = "id"
    name = "name"
    email = "email"
    role = "role"

# schema for outputting user format / payload
class UserPayload(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: UserRole

    class Config:
        from_attributes = True

# schema for input format of user signup api
class UserSignup(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: UserRole

# schema for input format of user update api
class UserUpdate(BaseModel):
    name: str
    email: EmailStr
    role: UserRole
    password: str

    class Config:
        form_attributes = True
