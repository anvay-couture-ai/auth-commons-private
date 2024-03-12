from pydantic import BaseModel, EmailStr
from typing import Optional, Union
import datetime

""" Base pydantic models """


class UserBase(BaseModel):
    """User schema without joined fields"""
    id: Optional[str]
    username: Optional[str]
    email: Optional[EmailStr]
    active: Optional[bool] = True
    birthdate: Optional[Union[datetime.datetime, None]]
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]
    last_login: Optional[Union[datetime.datetime, None]]

    class Config:
        orm_mode = True


class RoleBase(BaseModel):
    """Role schema without joined fields"""
    id: Optional[str]
    name: Optional[str]
    active: Optional[bool] = True

    class Config:
        orm_mode = True

class Token(BaseModel):
    """READ model for obtaining JWT"""
    access_token: str
    token_type: str

class GroupBase(BaseModel):
    """Group schema without joined fields"""
    name: Optional[str]
    active: Optional[bool] = True

    class Config:
        orm_mode = True


class PermissionBase(BaseModel):
    """Permission schema without joined fields"""
    name: str
    object: str
    description: Optional[str]

    class Config:
        orm_mode = True


class PolicyBase(BaseModel):
    """Policy schema without joined fields"""
    id: Optional[str]
    name: Optional[str]
    active: Optional[bool]
    description: Optional[str]

    class Config:
        orm_mode = True

