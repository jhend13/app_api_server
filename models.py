from datetime import datetime
from typing import List
from sqlalchemy import DateTime
from sqlalchemy import BigInteger
from sqlalchemy import String
from sqlalchemy import func
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
# from sqlalchemy.dialects.postgresql import JSONB
from .db import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    firebase_uid: Mapped[str] = mapped_column(String(128), unique=True)
    name: Mapped[str] = mapped_column(String(50))
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.current_timestamp())
    locations: Mapped[List['Location']] = relationship(back_populates='user')


class Location(Base):
    __tablename__ = 'locations'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped['User'] = relationship(back_populates='locations')
    full_address: Mapped[String] = mapped_column(String(200))


class Ride(Base):
    __tablename__ = 'rides'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    rider_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    driver_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    destination: Mapped[str] = mapped_column()
    origin: Mapped[str] = mapped_column()
    start: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.current_timestamp())
    end: Mapped[datetime] = mapped_column()
