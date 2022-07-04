from datetime import datetime
from typing import Optional,List
from unicodedata import category
from pydantic import BaseModel, EmailStr
from enum import Enum
from pydantic.types import conint


class Gender(str,Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"


class UserCreate(BaseModel):
    first_name: str
    last_name:str
    gender: Gender 
    email: EmailStr
    password: str

class UserOutput(BaseModel):
    id : int
    email : EmailStr
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
    id : Optional[str] = None

class Email(BaseModel):
    email: EmailStr

class Password(BaseModel):
    password: str

class ProductIn(BaseModel):
    name: str
    category:str
    price:str

class ProductOut(BaseModel):
    name:str
    category:str
    price:str
    created_at: datetime
    owner_id: int
    owner: UserOutput
    class Config:
        orm_mode = True

class Product(BaseModel):
    Product: ProductOut
    likes: int

    class Config:
        orm_mode = True



class Like(BaseModel):
    product_id:int
    der: conint(le=1)
