from datetime import datetime
from uuid import UUID

from fastapi import Depends

from config.celery import app
from services.feed_service import get_feed_service

@app.task
def test_task():
    print("Test task in process ...")


@app.task
async def update_feed(author_id: UUID,
                      header: str,
                      creation_date: datetime,
                      content: str | None,
                      feed_service: Depends(get_feed_service)):
    await feed_service.add(author_id=author_id,
                           header=header,
                           creation_date=creation_date,
                           content=content
                           )