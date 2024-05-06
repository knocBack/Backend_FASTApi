from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import database, oauth2, utils
from ..models import User,Product,Order,OrderItem
from ..schemas import user_schema,product_schema,order_schema
from typing import List

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.post('/products/add', response_model=product_schema.ProductPayload)
def add_product(product_info: product_schema.ProductCreate, db:Session = Depends(database.get_db), current_user: User = Depends(oauth2.get_current_user)):
    try:
        if current_user.role != user_schema.UserRole.admin:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"User is unauthorized")
        
        new_product = Product(**product_info.model_dump())
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        return new_product
    except HTTPException as http_err:
        raise http_err
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err))
 
@router.put("/products/update", response_model=product_schema.ProductPayload)
def update_product(product_info: product_schema.ProductPayload, db: Session=Depends(database.get_db), current_user: User = Depends(oauth2.get_current_user)):
    try:
        if current_user.role != user_schema.UserRole.admin:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"User is unauthorized")
        
        product = db.query(Product).filter(Product.id == product_info.id).first()
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id: {id} does not exist")
        
        product.name = product_info.name
        product.description = product_info.description
        product.price = product_info.price
        product.category = product_info.category

        db.commit()
        db.refresh(product)

        return product
    except HTTPException as http_err:
        raise http_err
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err))
    

@router.delete("/products/{product_id}", response_model= product_schema.ProductPayload)
def delete_product(product_id: int, db: Session=Depends(database.get_db), current_user: User = Depends(oauth2.get_current_user)):
    try:
        if current_user.role != user_schema.UserRole.admin:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"User is unauthorized")
        
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id: {product_id} does not exist")
        
        db.delete(product)
        db.commit()
        # db.refresh(product)

        return product
    except HTTPException as http_err:
        raise http_err
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err))
   


@router.get("/users/", response_model=List[user_schema.UserPayload])
def get_users(
    db: Session = Depends(database.get_db),
    current_user: user_schema.UserPayload = Depends(oauth2.get_current_user),
):
    try:
        if current_user.role != user_schema.UserRole.admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only admins can access this endpoint.",
            )

        users = db.query(User).all()
        return users

    except HTTPException as http_err:
        raise http_err
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err)
        )


@router.get("/users/search", response_model=List[user_schema.UserPayload])
def search_users(
    query: str,
    db: Session = Depends(database.get_db),
    current_user: user_schema.UserPayload = Depends(oauth2.get_current_user),
):
    try:
        if current_user.role != user_schema.UserRole.admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only admins can access this endpoint.",
            )

        users = db.query(User).filter(User.name.ilike(f"%{query}%")).all()
        return users

    except HTTPException as http_err:
        raise http_err
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err)
        )


@router.get("/users/sort", response_model=List[user_schema.UserPayload])
def sort_users(
    field: user_schema.UserSortFields,
    db: Session = Depends(database.get_db),
    current_user: user_schema.UserPayload = Depends(oauth2.get_current_user),
):
    try:
        if current_user.role != user_schema.UserRole.admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only admins can access this endpoint.",
            )

        users = db.query(User).order_by(getattr(User, field)).all()
        return users

    except HTTPException as http_err:
        raise http_err
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err)
        )


@router.get("/users/filter", response_model=List[user_schema.UserPayload])
def filter_users(
    role: user_schema.UserRole,
    db: Session = Depends(database.get_db),
    current_user: user_schema.UserPayload = Depends(oauth2.get_current_user),
):
    try:
        if current_user.role != user_schema.UserRole.admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only admins can access this endpoint.",
            )

        users = db.query(User).filter(User.role == role).all()
        return users

    except HTTPException as http_err:
        raise http_err
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err)
        )

@router.get("/orders/user/{user_id}", response_model=List[order_schema.OrderPayload])
def get_orders_by_user(
    db: Session = Depends(database.get_db),
    current_user: user_schema.UserPayload = Depends(oauth2.get_current_user)
):
    try:
        if current_user.role != user_schema.UserRole.admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only admins can access this endpoint.",
            )
        orders = db.query(Order).filter(Order.user_id == current_user.id).all()
        return orders

    except HTTPException as http_err:
        raise http_err
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err))

@router.patch("/orders/{order_id}", response_model=order_schema.OrderPayload)
def update_order_delivery_status(
    order_id: int,
    delivery_status: bool,
    db: Session = Depends(database.get_db),
    current_user: user_schema.UserPayload = Depends(oauth2.get_current_user)
):
    try:
        db_order = db.query(Order).filter(Order.id == order_id).first()
        if not db_order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order with id: {order_id} does not exist")

        if current_user.role != user_schema.UserRole.admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only admins can update delivery status.",
            )

        db_order.delivery_status = delivery_status
        db.commit()
        db.refresh(db_order)
        return db_order
        
    except HTTPException as http_err:
        raise http_err
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err))
