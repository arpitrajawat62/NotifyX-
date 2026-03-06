from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user import CreateUser
from app.schemas.auth import Token
from app.db.models import User
from starlette import status

from app.db.database import db_dependency
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from app.core.security import ALGORITHM, SECRET_KEY, bcrypt_context, hash_password

from app.services.auth_services import login_user


router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)



oauth2_bearer = OAuth2PasswordBearer(tokenUrl= '/auth/token')



  
async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user.')
        return {'username':username, 'id': user_id}
    except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user.')



@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency,create_user_request: CreateUser):
    create_user_model = User(
        username=create_user_request.username,
        email=create_user_request.email,
        hashed_password=hash_password(create_user_request.password),
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role
    )
    db.add(create_user_model)
    db.commit()
    return {"message": "User created successfully"}

    
@router.post("/token", response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
     return login_user(form_data.username, form_data.password, db)
