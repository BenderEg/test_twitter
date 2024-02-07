from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class UserInModel(BaseModel):

    name: Optional[str] = None


class UserOutModel(BaseModel):

    id: UUID
    name: Optional[str] = None
    creation_date: datetime