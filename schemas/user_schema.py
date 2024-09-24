# app/schemas/user_schema.py
from pydantic import BaseModel, EmailStr
from typing import Optional

# Schema for user creation
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

# Schema for reading user details (response)
class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True

# Schema for updating user details
class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    
class UserLogin(BaseModel):
    username: str
    password: str
