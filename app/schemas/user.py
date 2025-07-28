from pydantic import BaseModel, EmailStr, constr
from typing import Optional

class UserBase(BaseModel):
    username: constr(min_length=3, max_length=50)
    email: EmailStr

class UserCreate(UserBase):
    pass

class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    username: Optional[constr(min_length=3, max_length=50)] = None
    email: Optional[EmailStr] = None
