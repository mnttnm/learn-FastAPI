from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

from pydantic.types import conint

# schema from pydantic, getting used in our path operation
# it is different than the SQL alchemy model.
# if defines the structure of request and response


class UserOut(BaseModel):
    email: EmailStr
    id: int
    created_at: datetime

    # required so that pydentic can read the model response and convert it to dict
    class Config:
        orm_mode = True

# controls how the post in the response will be formatted
# out of all the fields that we get from a table entry what all should
# be returned to the user


# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool = True


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    created_at: datetime
    id: int
    owner_id: int
    owner: UserOut

    # required so that pydentic can read the model response and convert it to dict
    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)


class PostAndVotes(BaseModel):
    Post: PostResponse
    votes: int

    # required so that pydentic can read the model response and convert it to dict
    class Config:
        orm_mode = True
