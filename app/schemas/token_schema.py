from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# JWT Token Base Model
class Token(BaseModel):
    access_token: str
    token_type: str

# JWT token data
class TokenData(BaseModel):
    id: Optional[int] = None