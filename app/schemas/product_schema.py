from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from enum import Enum

# Product API Related Schemas

# schema for product creation input json
class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    category: str

    class Config:
        from_attributes = True

# schema for outputting product / payload
class ProductPayload(ProductCreate):
    id: int
    
    class Config:
        form_attributes = True

# emun for allowed sort fields in product sort api
class AllowedSortFields(str, Enum):
    id = "id"
    name = "name"
    description = "description"
    price = "price"
    category = "category"

# emun for allowed category fields in product filter api
class AllowedCategoryFields(str, Enum):
    food = "food",
    general = "general",
    survival = "survival",
    sports = "sports",
    stationary = "stationary"