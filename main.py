from fastapi import FastAPI, Depends, APIRouter, Request
from src.dependencies import UserDependency
from src.models import User
from src.schemas import UserBase, Token
from fastapi.security import OAuth2PasswordRequestForm
from src.jwt import create_access_token
from src.decorators import AccessDecorator
app = FastAPI(
    docs_url="/doc",
    title="FastAPI Demo",
    description="This is a very fancy project, with auto docs for the API and everything",
    version="0.0.1",
    redoc_url="/redoc"
)


user_dependency = UserDependency()
access = AccessDecorator(user_dependency)
auth_router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
    responses={
        404: {"description": "URL not found"},
        400: {"description": "Bad request"}
    },
)

auth_router.add_api_route(
    '/token',
    user_dependency.login_for_access_token,
    response_model=Token,
    summary='Authenticate via JWT Bearer scheme',
    methods=['post']
)
app.include_router(auth_router)

@app.get("/me", dependencies=[Depends(user_dependency.get_user_from_token)])
@access.is_authenticated
async def root(request: Request, user: UserBase = Depends(user_dependency.get_user_from_token)):
    print(user.__dict__)
    # print(request)
    
    
    return user.__dict__

@app.get("/is_authenticated", dependencies=[Depends(user_dependency.get_user_from_token)])
@access.is_authenticated
async def isAuthenticated(request: Request):
    return {"message": "User is authenticated"}