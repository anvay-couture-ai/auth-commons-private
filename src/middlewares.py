from datetime import datetime, timedelta
from fastapi import Request, Depends
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from .dependencies import UserDependency
# from src.dependencies import get_user_from_token
class AuthenticationMiddleware(BaseHTTPMiddleware):

    def __init__(self, app, user_dependency, include_routes = None):
        super().__init__(app)
        self.user_dependency = user_dependency
        self.include_routes = include_routes
        # Dictionary to store request counts for each IP
        # self.request_counts = {}

    async def dispatch(self, request, call_next):
        # Get the client's IP address
        print('Middleware')
        #print request body

        # get request headers
        if request.scope['path'] == '/auth/token' or request.scope['path'] == '/docs' or request.scope['path'] == '/redoc' or request.scope['path'] == '/openapi.json' or request.scope['path'] == '/favicon.ico' or request.scope['path'] == '/':
            return await call_next(request)
        try:
            token = request.headers.get('authorization', str()).split(' ')[1]
            print(f"token {token}")

            user = await self.user_dependency.get_user_from_token(token)

            if not user:
                return JSONResponse(status_code=401, content={"message": "Invalid token"})
        except IndexError:
            if request.scope['path'] in self.include_routes:
                return JSONResponse(status_code=401, content={"message": "Invalid token"})
            request.state.authorized = False
            response = await call_next(request)
            return response

        request.state.user = user
        request.state.authorized = True
        response = await call_next(request)
        return response
