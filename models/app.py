from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db import Base
from models.subscriber import Subscriber


class App(Base):
    __tablename__ = "apps"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    owner_email = Column(Integer, ForeignKey("users.email"))

    owner = relationship("User", back_populates="apps")
    subscribers = relationship("Subscriber", back_populates="app")
