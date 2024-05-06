from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from enum import Enum
from pydantic import BaseModel
from typing import List
from datetime import datetime, timezone
from .user_schema import UserPayload

# Order API Related Schemas

# enum for order sort-api fields
class OrderSortField(str, Enum):
    id = "id"
    order_date = "order_date"
    order_total = "order_total"
    delivery_status = "delivery_status"

# enum for order delivery statuses
class OrderDeliveryStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    delivered = "delivered"
    cancelled = "cancelled"

# Base Schema for Order Item
class OrderItemBase(BaseModel):
    product_id: int
    quantity: int
    unit_price: float

    class Config:
        from_attributes = True

# Just created for convient name
class OrderItemCreate(OrderItemBase):
    pass

# Order Item Schema
class OrderItem(OrderItemBase):
    id: int
    order_id: int

    class Config:
        from_attributes = True

# Base schema for Order
class OrderBase(BaseModel):
    # user_id: int
    order_date: datetime = datetime.now(timezone.utc)
    order_total: float
    delivery_status: bool = False
    order_items: List[OrderItemCreate]

    class Config:
        from_attributes = True

# schema for order creation api
class OrderCreate(OrderBase):
    order_date: datetime = datetime.now(timezone.utc)
    order_total: float
    order_items: List[OrderItemCreate]

    class Config:
        from_attributes = True

# schema for outputting orders / payload
class OrderPayload(OrderBase):
    id: int
    user: UserPayload
    order_items: List[OrderItem]

    class Config:
        from_attributes = True
