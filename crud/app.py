from pydantic import EmailStr
from sqlalchemy.orm import Session

from models import app as app_model
from schemas import app as app_schema


def get_apps(db: Session, skip: int = 0, limit: int = 100):
    apps = db.query(app_model.App).offset(skip).limit(limit).all()
    return apps


def get_app(db: Session, app_id: int):
    app = db.query(app_model.App).filter(app_model.App.id == app_id).first()
    return app


def post_app(app: app_schema.AppCreate, db: Session):
    db_app = app_model.App(name=app.name, owner_email=app.owner_email)
    db.add(db_app)
    db.commit()

    return db_app


def delete_app(db: Session, app_id: int):
    app = db.query(app_model.App).filter(app_model.App.id == app_id).first()
    db.delete(app)
    db.commit()


def get_apps_from_user_email(
    db: Session, email: EmailStr, skip: int = 0, limit: int = 100
):
    apps = (
        db.query(app_model.App)
        .filter(app_model.App.owner_email == email)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return apps
