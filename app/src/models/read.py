from fastapi import Query
from pydantic import BaseModel


class ReadQuery(BaseModel):
    read: bool = Query(default=True)


class ReadFilterQuery(BaseModel):
    read: bool | None = Query(default=None)