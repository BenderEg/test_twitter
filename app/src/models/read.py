from fastapi import Query
from pydantic import BaseModel


class ReadQuery(BaseModel):
    read: bool = Query(default=True)