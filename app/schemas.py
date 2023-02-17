from pydantic import BaseModel, EmailStr
from datetime import datetime


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