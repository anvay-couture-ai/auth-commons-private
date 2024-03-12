from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from jose import JWTError, jwt
from datetime import timedelta, datetime
from .models import User
from typing import Type, Union
import yaml
import os
from .utils import UnauthorizedException
with open(os.path.join(os.path.dirname(__file__), '../config.yaml')) as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None) -> str:
    """
    Creates JWT signed token from any payload, with expires time

    Args:
        data (dict): payload for token
        expires_delta (timedelta | None, optional): exp time in timedelta format.
        Defaults to None.

    Returns:
        str: JWT
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(seconds=config['Security']['jwt_ttl'])
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY,
                             algorithm=config['Security']['jwt_algorithm'])
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    """
    Decode string JWT token

    Args:
        token (str): JWT

    Raises:
        UnauthorizedException: when token is invalid

    Returns:
        dict: extracted payload
    """
    try:
        payload = jwt.decode(
            token, SECRET_KEY, algorithms=['HS256'])
    except JWTError:
        raise UnauthorizedException('Cannot decode token')
    else:
        return payload


def decode_auth_header(header: str) -> tuple[str, str]:
    try:
        chunks: list = header.split(' ')
        assert len(chunks) == 2, 'Bad header'
        return (chunks[0], chunks[1])
    except AssertionError as ex:
        raise UnauthorizedException(str(ex))
    except IndexError:
        raise UnauthorizedException('Wrong header payload')
