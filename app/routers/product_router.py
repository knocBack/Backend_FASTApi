from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from typing import List
from .. import utils, oauth2, database
from ..models import User,Product,Order,OrderItem
from ..schemas import user_schema, token_schema, product_schema
import traceback

# product router
router = APIRouter(
    prefix="/products",
    tags=['Products']
)

# search api
# can only search by name!
@router.get("/search", response_model=List[product_schema.ProductPayload])
def search_products(
    query: str | None = None,
    db: Session = Depends(database.get_db)
):
    try:
        print(query)
        products = db.query(Product).filter(Product.name.ilike(f"%{query}%")).all()
        return products
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err)
        )

# filter products
# - using category
@router.get("/filter", response_model=List[product_schema.ProductPayload])
def filter_products(
    category: str,
    db: Session = Depends(database.get_db)
):
    try:
        products = db.query(Product).filter(Product.category.ilike(f"%{category}%")).all()
        return products
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err)
        )

# sort products
# - any of the fields mentioned in prodduct_schema
@router.get("/sort", response_model=List[product_schema.ProductPayload])
def sort_products(
    field: product_schema.AllowedSortFields = product_schema.AllowedSortFields.id,
    db: Session = Depends(database.get_db)
):
    try:
        products = db.query(Product).order_by(getattr(Product, field)).all()
        return products
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err)
        )
    
# get all products
@router.get("/", response_model=List[product_schema.ProductPayload])
def get_all_products(db:Session = Depends(database.get_db)):
    try:
        product_info = db.query(Product).all()
        # if not product_info:
        #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id: {id} does not exist")
        # TODO - add limitters, upper limit and lower limit for the results!
        return product_info
    except HTTPException as http_err:
        raise http_err
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err))


# gets a single product by id
@router.get("/{id}", response_model=product_schema.ProductPayload)
def get_product(id: int, db:Session = Depends(database.get_db)):
    try:
        product_info = db.query(Product).filter(Product.id == id).first()
        # check if product id is invalid!
        if not product_info:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id: {id} does not exist")
        
        return product_info
    except HTTPException as http_err:
        raise http_err
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err))
     
