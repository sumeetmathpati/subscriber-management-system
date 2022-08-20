from typing import List, Union

from fastapi import APIRouter, Depends, HTTPException
from pydantic import EmailStr
from sqlalchemy.orm import Session

import dependencies
from crud import subscriber as subscribers_crud
from dependencies.user import get_db
from models import subscriber as subscription_model
from schemas import subscriber as subscription_schema

router = APIRouter(tags=["subscription"])


@router.get(
    "/subscriber",
    response_description="Get all the subscribers",
    response_model=List[subscription_schema.Subscriber],
)
async def get_subscribers(db: Session = Depends(dependencies.db.get_db)):
    subscribers = subscribers_crud.get_subscribers(db=db)
    return subscribers


@router.post(
    "/subscriber",
    response_description="Post Subscriber",
    response_model=Union[subscription_schema.Subscriber],
    status_code=201,
)
async def post_subscriber(subscriber: subscription_schema.SubscriberCreate, db: Session = Depends(get_db)):
    try:
        subscriber = subscribers_crud.post_subscribers(subscriber=subscriber, db=db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Cannot create subscriber because, {e}'")
    return subscriber


# @router.get("/subscription", response_description="Get all the subscriptions", response_model=List[Subscription])
# async def get_subscriptions():
#     subscriptions = await subscription_db.find().to_list(1000)
#     return subscriptions


# @router.post("/subscription", response_description="Add new subscription.", response_model=str)
# async def post_subscription(subscription: SubscriptionPost):
#     print(subscription)
#     # subscription = jsonable_encoder(subscription)
#     # new_subscription = await subscription_db.insert_one(subscription)
#     # created_subscription = await subscription_db.find_one({"_id": new_subscription.inserted_id})
#     return "created_subscription"
