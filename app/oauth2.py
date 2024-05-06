from jose import JWTError, jwt, ExpiredSignatureError
from datetime import datetime, timedelta, timezone
from . import database, models
from .schemas import user_schema, token_schema
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
# ACCESS_TOKEN_EXPIRE_MINUTES = 1

def create_access_token(data: dict):
    try:
        to_encode = data.copy()

        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        exp_timestamp = expire.timestamp()

        to_encode.update({"exp": exp_timestamp})

        print(to_encode)

        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

        return encoded_jwt
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err))


def verify_access_token(token: str, credentials_exception):

    try:
        print(token)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)
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


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    try:
        credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                            detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

        token = verify_access_token(token, credentials_exception)

        user = db.query(models.User).filter(models.User.id == token.id).first()
        
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {token.id} does not exist")
        
        return user

    except HTTPException as http_err:
        raise http_err

    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err))


