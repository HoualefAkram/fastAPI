from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
from pydantic.types import conint


class UserBase(BaseModel):
    """User base"""


class UserOut(UserBase):
    id: int
    email: str
    created_at: datetime


class UserCreate(UserBase):
    email: EmailStr
    password: str


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime
    owner: UserOut


class PostOut(BaseModel):
    Post: Post
    votes: int


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)  # type: ignore
