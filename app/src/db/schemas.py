import uuid

from datetime import datetime
from typing import Annotated

from sqlalchemy import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import expression

from db.sqlalcem import Base

uuid_pk = Annotated[uuid.UUID, mapped_column(
    primary_key=True,
    server_default=expression.text(
        "uuid_generate_v4()"))]
timestamp = Annotated[datetime,
mapped_column(TIMESTAMP(timezone=True),
              server_default=expression.text("TIMEZONE('utc', now())"),
              nullable=False)]
timestamp_upd = Annotated[datetime,
mapped_column(TIMESTAMP(timezone=True),
              onupdate=datetime.utcnow,
              server_default=expression.text("TIMEZONE('utc', now())"),
              nullable=False)]

class User(Base):
    __tablename__ = 'users'

    id: Mapped[uuid_pk]
    name: Mapped[str] = mapped_column(blank=True, nullable=True)
    creation_date: Mapped[timestamp]
    modified: Mapped[timestamp_upd]

    def __init__(self, name: str = None):
        self.name = name

    def __str__(self) -> str:
        return f'<User {self.id}>'