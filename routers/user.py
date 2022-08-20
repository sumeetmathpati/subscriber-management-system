import sqlite3
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import EmailStr
from sqlalchemy.orm import Session

import crud.user as user_crud
import dependencies
from schemas import user as user_schema

router = APIRouter(tags=["users"])


@router.get("/user/me", response_model=List[user_schema.User])
async def get_me(
    current_user: user_schema.User = Depends(dependencies.user.get_current_active_user),
):
    return current_user


# Get all users
@router.get("/user", response_model=List[user_schema.User])
async def get_users(
    skip: int = 0, limit: int = 100, db: Session = Depends(dependencies.db.get_db)
):
    users = user_crud.get_users(db, skip=skip, limit=limit)
    return users


@router.post("/user", response_model=user_schema.User)
async def post_user(
    user: user_schema.UserCreate, db: Session = Depends(dependencies.db.get_db)
):
    try:
        user = user_crud.post_user(user=user, db=db)
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail=f"Email already exists!")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Cannot create user, {e}")
    return user


# Get single user
@router.get("/user/{user_id}", response_model=user_schema.User)
async def get_user(user_id: int, db: Session = Depends(dependencies.db.get_db)):
    db_user = user_crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/user/{email}", response_model=user_schema.User)
async def get_user_from_email(
    email: EmailStr, db: Session = Depends(dependencies.db.get_db)
):
    db_user = user_crud.get_user_from_email(db, email=email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.delete("/user/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(dependencies.db.get_db)):
    user_crud.delete_user(user_id=user_id, db=db)
    return ""
