from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# to hash the password_string
def hash(password: str):
    return pwd_context.hash(password)

# to verify if the password_string and hashed_password matches
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
