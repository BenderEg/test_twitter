import uuid

from datetime import datetime
from typing import Annotated, Optional

from sqlalchemy import TIMESTAMP, ForeignKeyConstraint, UniqueConstraint
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
    name: Mapped[Optional[str]]
    creation_date: Mapped[timestamp]
    modified: Mapped[timestamp_upd]

    def __init__(self, name: str = None):
        self.name = name

    def __str__(self) -> str:
        return f'<User {self.id}>'

    def dict(self) -> dict:
        return {"id": self.id,
                "name": self.name,
                "creation_date": self.creation_date
                }


class Subscription(Base):
    __tablename__ = 'subscriptions'

    id: Mapped[uuid_pk]
    user_id: Mapped[uuid.UUID]
    subscriber_id: Mapped[uuid.UUID]
    creation_date: Mapped[timestamp]

    __table_args__ = (
        ForeignKeyConstraint(["user_id"], ["users.id"]),
        ForeignKeyConstraint(["subscriber_id"], ["users.id"]),
        UniqueConstraint('user_id', 'subscriber_id', name='user_subscriber_idx'),
    )

    def __init__(self, user_id: uuid.UUID, subscriber_id: uuid.UUID):
        self.user_id = user_id
        self.subscriber_id = subscriber_id

    def __str__(self) -> str:
        return f'<User {self.user_id} subscribed on {self.subscriber_id}>'

    def dict(self) -> dict:
        return {"id": self.id,
                "user_id": self.user_id,
                "subscriber_id": self.subscriber_id,
                "creation_date": self.creation_date
                }