from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from enum import Enum

class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    category: str

    class Config:
        from_attributes = True

class ProductPayload(ProductCreate):
    id: int
    
    class Config:
        form_attributes = True

class AllowedSortFields(str, Enum):
    id = "id"
    name = "name"
    description = "description"
    price = "price"
    category = "category"

class AllowedCategoryFields(str, Enum):
    food = "food",
    general = "general",
    survival = "survival",
    sports = "sports",
    stationary = "stationary"