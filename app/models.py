from sqlalchemy import Column, Integer, String, Text, Boolean, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime, timezone


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False, index=True)

    user_orders = relationship("Order", back_populates="user")


class Product(Base):
    __tablename__ ="products"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    name = Column(String, nullable = False, index=True)
    description = Column(Text, nullable = True)
    price = Column(Float, nullable = False)
    category = Column(String, nullable = True, index=True)


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    order_date = Column(DateTime, default=datetime.now(timezone.utc), nullable=False, index=True)
    order_total = Column(Float, nullable = False)
    delivery_status = Column(String, default = "pending", nullable=False)

    user = relationship("User", back_populates="user_orders")
    order_items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)

    product = relationship("Product")
    order = relationship("Order", back_populates="order_items")