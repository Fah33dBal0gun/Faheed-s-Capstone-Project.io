from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True

class MovieBase(BaseModel):
    title: str
    description: Optional[str] = None

class MovieCreate(MovieBase):
    pass

class MovieOut(MovieBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

class CommentBase(BaseModel):
    text: str

class CommentCreate(CommentBase):
    pass

class CommentOut(CommentBase):
    id: int
    movie_id: int
    user_id: int

    class Config:
        orm_mode = True