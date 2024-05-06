from jose import JWTError, jwt, ExpiredSignatureError
from datetime import datetime, timedelta, timezone
from . import database, models
from .schemas import user_schema, token_schema
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

# mentioning that tokenUrl is generated from /login endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
# ACCESS_TOKEN_EXPIRE_MINUTES = 1

# this function creates JWT access token
def create_access_token(data: dict):
    try:
        to_encode = data.copy()

        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        exp_timestamp = expire.timestamp() # expiry timestamp  needs to be in utc

        to_encode.update({"exp": exp_timestamp}) # expiry timestamp should be given in "exp" key only!

        print(to_encode)

        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) # JWT encoded

        return encoded_jwt
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err))


# this function verifies if the given token is valid
    # catches ExpiredSignatureError -> token has expired
    # catches JWT error -> token is invalid
def verify_access_token(token: str, credentials_exception):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: int = payload.get("user_id")
        if id is None:
            raise credentials_exception
        
        token_data = token_schema.TokenData(id=id)

    except ExpiredSignatureError:
        # Handle token expiration (ExpiredSignatureError)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )

    except JWTError:
        token_data = token_schema.TokenData()
        raise credentials_exception
    
    return token_data


# this fucntion returns the current user, after verifying
# fetches user_id from the JWT token!
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    try:
        credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                            detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

        token = verify_access_token(token, credentials_exception) #verify JWT

        user = db.query(models.User).filter(models.User.id == token.id).first() # find user
        
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {token.id} does not exist") # token error
        
        return user

    except HTTPException as http_err:
        raise http_err

    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err))


