from datetime import timedelta
from typing import Optional

from fastapi import BackgroundTasks, HTTPException
from starlette import status
from sqlalchemy.orm import Session

from app.db.models import User
from app.core.security import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    verify_password,
    create_access_token,
)

from app.schemas.auth import Token
from app.services.email_sender import send_email


def authenticate_user(username: str, password: str, db: Session) ->  Optional[User]:
    user = db.query(User).filter(User.username == username).first()

    if not user or not verify_password(password, user.hashed_password):
        return None
    
    return user


def login_user(username: str, password: str, db: Session, background_tasks: BackgroundTasks):

    user = authenticate_user(username, password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    background_tasks.add_task(
        send_email,
        user.email,
        "Login Alert",
        f"Hello {user.username}, you logged in successfully."
    )
 
    access_token = create_access_token(
        username=user.username,
        user_id=user.id,
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return Token(
        access_token=access_token,
        token_type="bearer"
    )