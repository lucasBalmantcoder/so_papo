from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime


# ----------------- JWT Token Schema -------------------

class JwtTokenSchema(BaseModel):
    token: str
    payload: dict
    expires: datetime


class TokenPair(BaseModel):
    access: JwtTokenSchema
    refresh: JwtTokenSchema


# ----------------- User Schema -------------------

class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: str
    created_at: datetime


class UserLogin(BaseModel):
    username: str
    password: str


# ----------------- Token Blacklist Schema -------------------

class BlackListTokenSchema(BaseModel):
    id: str
    token: str
    created_at: datetime
