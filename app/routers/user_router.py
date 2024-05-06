from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from .. import utils, oauth2, database
from ..models import User,Product,Order,OrderItem
from ..schemas import user_schema, token_schema
import traceback

# user router
router = APIRouter(
    prefix="/users",
    tags=['Users']
)

# login api 
# - authenticates user and 
# - creates JWT token for authorization
@router.post('/login', response_model=token_schema.Token)
def login(user_credentials: OAuth2PasswordRequestForm=Depends(), db:Session = Depends(database.get_db)):
    try:
        user = db.query(User).filter(
            User.email == user_credentials.username # returns email
        ).first()
        
        # invalid username / email
        if not user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Invalid Username"
            )
        
        # invalid credentials
        if not utils.verify(user_credentials.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Invalid Credentials"
            )

        # JWT payload
        details = {
            "user_id": user.id,
            "user_role": user.role
        }
        access_token = oauth2.create_access_token(data=details) # token created
        
        # return JWT to the client
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
    except HTTPException as http_err:
        raise http_err
    except Exception as err:
        traceback_str = traceback.format_exc()
        raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"error":str(err),"traceback":traceback_str}
            )

# signup api
@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=user_schema.UserPayload)
def signup(user: user_schema.UserSignup, db:Session=Depends(database.get_db)):
    try:
        found_user = db.query(User).filter(User.email==user.email).first()
        if found_user: # email exists already!
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User with email: {found_user.email} already exist")

        # hashing password to store!
        hashed_password = utils.hash(user.password)
        user.password = hashed_password

        new_user = User(**user.model_dump())

        db.add(new_user)
        db.commit() # new user added
        db.refresh(new_user)

        return new_user
    except HTTPException as http_err:
        raise http_err
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err))

# get a single user
@router.get("/{id}", response_model=user_schema.UserPayload)
def get_user(id: int, db: Session = Depends(database.get_db)):
    try:
        user = db.query(User).filter(User.id == id).first()
        if not user: # user does not exist
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exist")
        
        return user
    except HTTPException as http_err:
        raise http_err
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err))
    
# update user info, only by user 
# - requires token
@router.put("/update", response_model=user_schema.UserPayload)
def update_user(user: user_schema.UserUpdate, db: Session=Depends(database.get_db), current_user: User = Depends(oauth2.get_current_user)):
    try:   
        found_user = db.query(User).filter(User.email==user.email).first()
        # check if the new email is already in use!
        if found_user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User with email: {found_user.email} already exist")
        
        current_user.name = user.name
        current_user.email = user.email
        current_user.password = utils.hash(user.password) # store hashed password
        current_user.role = user.role

        db.commit()

        db.refresh(current_user)

        return current_user
    except HTTPException as http_err:
        raise http_err
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err))
    
# delete user 
# - requires token
@router.delete("/delete", response_model= user_schema.UserPayload)
def delete_user(db: Session=Depends(database.get_db), current_user: User = Depends(oauth2.get_current_user)):
    try:
        
        db.delete(current_user)
        db.commit()
        db.refresh(current_user)

        return current_user
    except HTTPException as http_err:
        raise http_err
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err))
    