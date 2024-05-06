from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from typing import List
from .. import utils, oauth2, database
from ..models import User,Product,Order,OrderItem
from ..schemas import user_schema, token_schema, product_schema, order_schema
import traceback

#order router
router = APIRouter(
    prefix="/orders",
    tags=['Orders']
)

# function to validate order total with all the order_items in the placed order
def validate_order_total(order: order_schema.OrderCreate):
    price = 0.0
    for item in order.order_items:
        price+=(item.quantity*item.unit_price)

    return price==order.order_total

# function to validate all the products in the order_items
def validate_products(order_items: List[order_schema.OrderItem], db: Session):
    for item in order_items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            return False
        
    return True

# create order api
# - requires token
@router.post("/", response_model=order_schema.OrderPayload)
def create_order(
    order: order_schema.OrderCreate,
    db: Session = Depends(database.get_db),
    current_user: user_schema.UserPayload = Depends(oauth2.get_current_user)
):
    try:
        # check if all products are valid
        if not validate_products(order.order_items, db):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid products. Please check the order details."
            )
        # check if order total is correct
        if not validate_order_total(order):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid Order Total. Please check the order details."
            )
        
        # creating entries in order and order_items table
        order_items = [OrderItem(**item.model_dump()) for item in order.order_items]
        db_order = Order(**order.model_dump(exclude={"order_items"}), user_id = current_user.id, order_items=order_items)
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
        return db_order
    
    except HTTPException as http_err:
        raise http_err
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err))

# api to check user's orders
# - requires token
@router.get("/my_orders/", response_model=List[order_schema.OrderPayload])
def get_orders_by_user(
    db: Session = Depends(database.get_db),
    current_user: user_schema.UserPayload = Depends(oauth2.get_current_user)
):
    try:
        orders = db.query(Order).filter(Order.user_id == current_user.id).all()
        return orders

    except HTTPException as http_err:
        raise http_err
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err))

# get an order by id
# - requires token
@router.get("/{order_id}", response_model=order_schema.OrderPayload)
def read_order(
    order_id: int,
    db: Session = Depends(database.get_db),
    current_user: user_schema.UserPayload = Depends(oauth2.get_current_user)
):
    try:
        db_order = db.query(Order).filter(Order.id == order_id).first()
        if db_order is None:
            raise HTTPException(status_code=404, detail=f"Order with id: {order_id} does not exist")
        return db_order
    
    except HTTPException as http_err:
        raise http_err
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err))

# edit order details
# - requires token
@router.put("/{order_id}", response_model=order_schema.OrderPayload)
def update_order(
    order_id: int,
    order: order_schema.OrderCreate,
    db: Session = Depends(database.get_db),
    current_user: user_schema.UserPayload = Depends(oauth2.get_current_user)
):
    try:
        db_order = db.query(Order).filter(Order.id == order_id).first()
        # check if order exists
        if not db_order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order with id: {order_id} does not exist")
       
        # check if all products are valid
        if not validate_products(order.order_items, db):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid products. Please check the order details."
            )

        # validate order total
        if not validate_order_total(order):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid order total. Please check the order details."
            )

        db_order.user_id = current_user.id
        db_order.order_date = order.order_date
        db_order.order_total = order.order_total
        # db_order.delivery_status = order.delivery_status

        # existing_items = db.query(OrderItem).filter(order_id==order_id).all()
        # for item in existing_items:
        #     pass
        # TODO 

        # Update order items
        for item in order.order_items:
            existing_item = db.query(OrderItem).filter_by(order_id=order_id, product_id=item.product_id).first()
            if existing_item:
                existing_item.quantity = item.quantity
                existing_item.unit_price = item.unit_price
            else:
                new_item = OrderItem(**item.model_dump(), order_id=order_id)
                db.add(new_item)

        db.commit()
        db.refresh(db_order)
        return db_order
        
        
    except HTTPException as http_err:
        raise http_err
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err))

# delete an order #TODO - also add order-cancel!
# - requires token
@router.delete("/{order_id}", response_model=order_schema.OrderPayload)
def delete_order(
    order_id: int,
    db: Session = Depends(database.get_db),
    current_user: user_schema.UserPayload = Depends(oauth2.get_current_user)
):
    try:
        db_order = db.query(Order).filter(Order.id == order_id).first()
        if not db_order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order with id: {order_id} does not exist")
        db.delete(db_order)
        db.commit()
        return db_order
        
    except HTTPException as http_err:
        raise http_err
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err))

