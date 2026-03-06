from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
import os


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 20))

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def hash_password(password: str) -> str:
    return bcrypt_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt_context.verify(password, hashed_password)


def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    payload = {
        "sub": username,
        "id": user_id,
        "exp": datetime.utcnow() + expires_delta
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str):
    try:
       return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None
