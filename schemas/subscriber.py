from pydantic import BaseModel, EmailStr


class SubscriberBase(BaseModel):
    name: str
    email: EmailStr
    subscribed: bool = True
    app_id: int


class SubscriberCreate(SubscriberBase):
    pass


class Subscriber(SubscriberBase):
    id: int

    class Config:
        orm_mode = True
