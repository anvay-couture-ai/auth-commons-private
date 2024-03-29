from sqlalchemy import create_engine
from fastapi import Depends, Request
from sqlalchemy.orm import sessionmaker, relationship, joinedload
from sqlalchemy.ext.declarative import declarative_base
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from .jwt import decode_access_token, create_access_token
from .crpto import create_password_hash
from .models import User, M2MUserRole, M2MUserGroup, Role, Group, Permission, Policy, Sessions
import yaml
from fastapi.security import OAuth2PasswordBearer
from starlette.middleware.base import BaseHTTPMiddleware

from .schemas import UserBase, RoleBase, GroupBase, PermissionBase, PolicyBase

import os
import uuid
TOKEN_URL = "auth/token"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=TOKEN_URL)

# create an dependency injection container for getting user from the token
class UserDependency:
    TOKEN_URL = TOKEN_URL
    def __init__(self):
        # read from config.yaml in ../config.yaml
        with open(os.path.join(os.path.dirname(__file__), '../config.yaml')) as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
        # create engine
        engine = create_engine('postgresql://' + config['postgres']['user'] + ':' + config['postgres']['password'] + '@localhost:5432/' + config['postgres']['database'])
        Session = sessionmaker(bind=engine)
        self.session = Session()
    async def get_user_from_token(self, token: str = Depends(oauth2_scheme)):
        payload = decode_access_token(token)
        print(payload)
        user = self.session.query(User).filter(User.username == payload['sub']).first()
        print(user)
        return user
    
    async def authenticate_user(self, username: str, password: str):
        user = self.session.query(User).filter(User.username == username).first()
        # breakpoint()
        if user is None:
            return False
        if user.password == create_password_hash(password):
            return user
        
    async def get_all_users(self):
        users = self.session.query(User).all()
        return users
    
    async def login_for_access_token(self,  request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
        user = await self.authenticate_user(form_data.username, form_data.password)
        access_token = create_access_token(
            data={"sub": user.username})  # type: ignore
        return {"access_token": access_token, "token_type": "bearer"}


