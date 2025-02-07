from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy import func
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
# from sqlalchemy.dialects.postgresql import JSONB
from app.models.base import Base


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
