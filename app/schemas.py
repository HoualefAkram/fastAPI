from pydantic import BaseModel, EmailStr
from datetime import datetime


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    """User base"""


class UserCreate(UserBase):
    email: EmailStr
    password: str


class UserOut(UserBase):
    id: int
    email: str
    created_at: datetime

    class Config:
        orm_mode = True
