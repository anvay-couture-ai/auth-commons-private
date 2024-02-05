from fastapi import FastAPI, Depends, APIRouter, HTTPException, Request
from src.schemas import UserBase, Token
from fastapi.security import OAuth2PasswordRequestForm
from src.jwt import create_access_token
from src.dependencies import UserDependency
from src.middlewares import AuthenticationMiddleware




app = FastAPI(
    docs_url="/docs",
    title="FastAPI Demo",
    description="This is a very fancy project, with auto docs for the API and everything",
    version="0.0.1",
    redoc_url="/redoc"
)


# Add it to auth directory to get JWT token (Login Router)
user_dependency = UserDependency()

@app.post("/auth/token", response_model=Token, summary='Authenticate via JWT Bearer scheme')
async def get_access_token(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    return await user_dependency.login_for_access_token(request, form_data)


app.add_middleware(AuthenticationMiddleware, user_dependency=user_dependency)

# Implementation on APIs
@app.get("/me" #, dependencies=[Depends(user_dependency.get_user_from_token)]
         )
async def root(request: Request):
    return request.state.user.__dict__

