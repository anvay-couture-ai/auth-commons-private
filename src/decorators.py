from fastapi import Request
from functools import wraps

from .utils import UnauthorizedException

from .jwt import decode_auth_header
from .models import User
class AccessDecorator:
    def __init__(self, user_dependency):
        self.user_dependency = user_dependency
    
    def is_authenticated(self, func):
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            print('isAuthenticated')
            print(request)
            print(request.headers.get('authorization', str()))
            validator, token = decode_auth_header(
                    request.headers.get('authorization', str()))
            current_user: User = await self.user_dependency.get_user_from_token(token)
            if not current_user:
                raise UnauthorizedException('Invalid token')
            print(current_user.username)
            return await func(request, *args, **kwargs)
        return wrapper
    
    def has_permission(self, permission: str):
        def decorator(func):
            @wraps(func)
            async def wrapper(request: Request, *args, **kwargs):
                print('has_permission')
                print(request)
                print(request.headers.get('authorization', str()))
                validator, token = decode_auth_header(
                    request.headers.get('authorization', str()))
                current_user: User = await self.user_dependency.get_user_from_token(token)
                if not current_user:
                    raise UnauthorizedException('Invalid token')
                print(current_user.username)
                return await func(request, *args, **kwargs)
            return wrapper
        return decorator