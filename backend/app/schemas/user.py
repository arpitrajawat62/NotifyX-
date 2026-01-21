from typing import Optional
from pydantic import BaseModel, Field, EmailStr


class CreateUser(BaseModel):
    username: str
    first_name: str
    last_name: Optional[str] = None
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserResponse(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: Optional[str] 
    email: EmailStr
    role: str

