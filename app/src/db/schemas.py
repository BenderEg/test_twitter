import uuid

from datetime import datetime
from typing import Annotated, Optional

from sqlalchemy import TIMESTAMP, ForeignKeyConstraint, \
    UniqueConstraint, Index, PrimaryKeyConstraint
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
        ForeignKeyConstraint(["user_id"], ["users.id"], ondelete='CASCADE'),
        ForeignKeyConstraint(["subscriber_id"], ["users.id"], ondelete='CASCADE'),
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


class Post(Base):
    __tablename__ = 'posts'

    id: Mapped[uuid_pk]
    user_id: Mapped[uuid.UUID]
    header: Mapped[str]
    content: Mapped[Optional[str]]
    creation_date: Mapped[timestamp]

    __table_args__ = (
        ForeignKeyConstraint(["user_id"], ["users.id"], ondelete='CASCADE'),
        Index("user_id_idx", "user_id")
    )

    def __init__(self, user_id: uuid.UUID, header: str, content: str = None):
        self.user_id = user_id
        self.header = header
        self.content = content

    def __str__(self) -> str:
        return f'<{self.header}>'

    def dict(self) -> dict:
        return {"id": self.id,
                "user_id": self.user_id,
                "header": self.header,
                "content": self.content,
                "creation_date": self.creation_date
                }


class Feed(Base):
    __tablename__ = 'feeds'

    id: Mapped[uuid_pk]
    user_id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    author_id: Mapped[uuid.UUID]
    post_id: Mapped[uuid.UUID]
    header: Mapped[str]
    content: Mapped[Optional[str]]
    creation_date: Mapped[timestamp]
    read: Mapped[bool] = mapped_column(default=False, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint("user_id", "id"),
        ForeignKeyConstraint(["user_id"], ["users.id"], ondelete='CASCADE'),
        ForeignKeyConstraint(["author_id"], ["users.id"], ondelete='CASCADE'),
        ForeignKeyConstraint(["post_id"], ["posts.id"], ondelete='CASCADE'),
        Index("creation_date_idx", "creation_date"),
    )

    def __init__(self, user_id: uuid.UUID, author_id: uuid.UUID, post_id: uuid.UUID,
                 header: str, creation_date: datetime, content: str = None):
        self.user_id = user_id
        self.author_id = author_id
        self.post_id = post_id
        self.header = header
        self.content = content
        self.creation_date = creation_date

    def __str__(self) -> str:
        return f'<{self.id}>'

    def dict(self) -> dict:
        return {"id": self.id,
                "user_id": self.user_id,
                "author_id": self.author_id,
                "post_id": self.post_id,
                "header": self.header,
                "content": self.content,
                "creation_date": self.creation_date,
                "read": self.read
                }