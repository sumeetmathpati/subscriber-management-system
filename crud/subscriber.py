from pydantic import EmailStr
from sqlalchemy.orm import Session

from models import subscriber as subscription_model
from schemas import subscriber as subscriber_schema


def get_subscribers(db: Session, skip: int = 0, limit: int = 100):
    subscribers = (
        db.query(subscription_model.Subscriber).offset(skip).limit(limit).all()
    )
    return subscribers


def post_subscribers(db: Session, subscriber: subscriber_schema.SubscriberCreate):
    db_subscriber = subscription_model.Subscriber(
        name=subscriber.name, email=subscriber.email, app_id=subscriber.app_id
    )
    db.add(db_subscriber)
    db.commit()

    return db_subscriber
