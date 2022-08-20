from pydantic import BaseModel, EmailStr


class AppBase(BaseModel):
    name: str
    owner_email: EmailStr


class AppCreate(AppBase):
    pass


class App(AppBase):
    id: int

    class Config:
        orm_mode = True
