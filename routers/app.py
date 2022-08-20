from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import EmailStr
from sqlalchemy.orm import Session

import dependencies
from crud import app as app_crud
from dependencies.user import get_db
from schemas import app as app_schema

router = APIRouter(tags=["apps"])


# Get all users
@router.get("/app", response_model=List[app_schema.App])
async def get_apps(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    apps = app_crud.get_apps(db, skip=skip, limit=limit)
    return apps


@router.post("/app", response_model=app_schema.App)
async def post_app(app: app_schema.AppCreate, db: Session = Depends(get_db)):
    try:
        app = app_crud.post_app(app=app, db=db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Cannot create app because, {e}'")
    return app


# Get single user
@router.get("/app/{app_id}", response_model=app_schema.App)
async def get_app(app_id: int, db: Session = Depends(get_db)):
    db_app = app_crud.get_app(db, app_id=app_id)
    if db_app is None:
        raise HTTPException(status_code=404, detail="App not found")
    return db_app


@router.delete("/app/{app_id}")
async def delete_app(app_id: int, db: Session = Depends(dependencies.db.get_db)):
    app_crud.delete_app(app_id=app_id, db=db)
    return ""


@router.get("/app/user/{email}", response_model=List[app_schema.App])
async def get_user_apps(
    email: EmailStr, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    apps = app_crud.get_apps_from_user_email(db, skip=skip, limit=limit, email=email)
    return apps
