from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class PostInModel(BaseModel):

    user_id: UUID
    header: str = Field(..., max_length=140)
    content: Optional[str] = None


class PostOutModel(PostInModel):

    id: UUID
    creation_date: datetime


class FeedPostModel(PostInModel):

    id: UUID
    author_id: UUID
    post_id: UUID
    creation_date: datetime
    read: Optional[bool] = False


class DeletedPostModel(BaseModel):

    user_id: UUID
    post_id: UUID