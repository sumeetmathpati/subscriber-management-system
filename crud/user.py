from sqlalchemy.orm import Session

import utils.auth
from models import user as user_model
from schemas import user as user_schema


def get_users(db: Session, skip: int = 0, limit: int = 100):
    users = db.query(user_model.User).offset(skip).limit(limit).all()
    return users


def get_user(db: Session, user_id: int):
    user = db.query(user_model.User).filter(user_model.User.id == user_id).first()
    return user


def get_user_from_email(db: Session, email: str):
    user = db.query(user_model.User).filter(user_model.User.email == email).first()
    return user


def post_user(db: Session, user: user_schema.UserCreate):
    # Create hashed password
    hashed_password = utils.auth.get_password_hash(user.password)

    # Create a instance of DbUser to add.
    db_user = user_model.User(
        name=user.name, email=user.email, hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()

    return db_user


def delete_user(db: Session, user_id: int):
    user = db.query(user_model.User).filter(user_model.User.id == user_id).first()
    db.delete(user)
    db.commit()
