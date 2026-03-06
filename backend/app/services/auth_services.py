from datetime import timedelta
from typing import Optional
from app.db.models import User
from app.core.security import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    verify_password,
    create_access_token,
)
from fastapi import HTTPException
from starlette import status
from sqlalchemy.orm import Session
from app.schemas.auth import Token




def authenticate_user(username: str, password: str, db: Session) ->  Optional[User]:
    user = db.query(User).filter(User.username == username).first()

    if not user or not verify_password(password, user.hashed_password):
        return None
    
    return user


def login_user(username: str, password: str, db: Session) -> Token:

    user = authenticate_user(username, password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user.')
 
    token = create_access_token(
        user.username, 
        user.id, 
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return Token(
    access_token=token,
    token_type="bearer"
    )