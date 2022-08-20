from datetime import timedelta

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

# from dependencies import get_current_active_user
import dependencies
import utils
from db import Base, engine
from routers.app import router as app_router
from routers.subscriber import router as subscription_router
from routers.user import router as user_router
from schemas import auth, user

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_router)
app.include_router(app_router)
app.include_router(subscription_router)


@app.post("/token", response_model=auth.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    authenticated_user = utils.auth.authenticate_user(
        form_data.username, form_data.password
    )
    if not authenticated_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=utils.auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = utils.auth.create_access_token(
        data={"sub": authenticated_user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/")
async def root():
    return {"message": "Welcome to subscriber management system!"}


@app.get("/items/", response_model=user.User)
async def read_items(
    current_user: user.User = Depends(dependencies.user.get_current_active_user),
):
    return current_user
