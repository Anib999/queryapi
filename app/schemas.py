from pydantic import BaseModel, EmailStr, conint
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


class QueryBase(BaseModel):
    QueryName: str


class QueryCreate(QueryBase):
    pass


class QueryUpdate(QueryBase):
    QueryDescription: str
    company_id: int
    folder_id: int


class Query(QueryBase):
    QId: int
    QueryDescription: str

    class Config:
        orm_mode = True


class CommentBase(BaseModel):
    CommentDetail: str
    query_id: int
    # user_id: int


class CommentCreate(CommentBase):
    pass


class Comment(CommentBase):
    user_id: int
    user: User
    # query: QueryBase

    class Config:
        orm_mode = True

class LikeBase(BaseModel):
    comment_id: int
    comment_dir: conint(ge=0, le=1)

class LikeCreate(LikeBase):
    pass

class Like(LikeBase):

    class Config:
        orm_mode = True

class CommentLike(BaseModel):
    Comment: Comment
    LikeCount: int

    class Config:
        orm_mode = True