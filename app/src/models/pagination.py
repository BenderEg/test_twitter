from fastapi import Query
from pydantic import BaseModel


class Pagination(BaseModel):
    limit: int = Query(ge=1, le=200, default=50)
    offset: int = Query(ge=0, default=0)