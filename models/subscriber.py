from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from db import Base


class Subscriber(Base):
    __tablename__ = "subscribers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(Integer, index=True)
    subscribed = Column(Boolean, default=True)
    app_id = Column(Integer, ForeignKey("apps.id"))

    app = relationship("App", back_populates="subscribers")
