from datetime import datetime
from http import HTTPStatus
from uuid import UUID

import asyncio

from fastapi import APIRouter, Depends, BackgroundTasks

from models.posts import PostInModel, PostOutModel
from services.feed_service import FeedService, get_feed_service
from services.post_service import PostService, get_post_service

router = APIRouter()


async def test_task(author_id: UUID,
                    header: str,
                    creation_date: datetime,
                    content: str | None,
                    service: FeedService):
    await asyncio.sleep(60)
    await service.add(author_id, header, creation_date, content)


@router.post("/", status_code=HTTPStatus.CREATED,
             response_model=PostOutModel)
async def create_post(post_in: PostInModel,
                      background_tasks: BackgroundTasks,
                      post_service: PostService = Depends(get_post_service),
                      feed_service: FeedService = Depends(get_feed_service)) -> PostOutModel:
    post = await post_service.create(post_in.user_id, post_in.header, post_in.content)
    # start background celery task for feed update
    background_tasks.add_task(test_task, post.user_id, post.header, post.creation_date, post.content, feed_service)
    return PostOutModel(**post.dict())