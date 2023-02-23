from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class CompanyBase(BaseModel):
    # id: Optional[int] = 0
    CompanyName: str
    DatabaseName: str


class CompanyCreate(CompanyBase):
    pass


class Company(CompanyBase):
    created_at: datetime

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: EmailStr
    password: str


class UserCreate(UserBase):
    pass


class User(BaseModel):
    UId: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    UId: Optional[str] = None

class CommentBase(BaseModel):
    CommentDetail: str
    query_id: int
    user_id: int


class CommentCreate(CommentBase):
    pass

class Comment(CommentBase):

    class Config:
        orm_mode = True

class FolderBase(BaseModel):
    FolderName: str

class ShowFolder(FolderBase):
    FId: int

    class Config:
        orm_mode = True

class FolderCreate(FolderBase):
    pass

class Folder(FolderBase):
    class Config:
        orm_mode = True
