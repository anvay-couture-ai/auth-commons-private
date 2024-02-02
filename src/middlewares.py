from datetime import datetime, timedelta
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
# from src.dependencies import get_user_from_token

class AuthenticationMiddleware(BaseHTTPMiddleware):

    def __init__(self, app, user_dependency):
        super().__init__(app)
        self.user_dependency = user_dependency
        # Dictionary to store request counts for each IP
        # self.request_counts = {}

    async def dispatch(self, request, call_next):
        # Get the client's IP address
        print('Middleware')
        #print request body
        print(request.__dict__['scope'].keys())

        # get request headers
        try:
            token = request.headers.get('authorization', str()).split(' ')[1]
            print(f"token {token}")

            user = self.user_dependency.get_user_from_token(token)
            print(user)

            if not user:
                return JSONResponse(status_code=401, content={"message": "Invalid token"})
        except IndexError:
            return JSONResponse(status_code=400, content={"message": "Bad header"})





  
        # Proceed with the request
        response = await call_next(request)
        return response
