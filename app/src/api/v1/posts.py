from http import HTTPStatus

from fastapi import APIRouter, Depends

from background.tasks import update_feed
from models.posts import PostInModel, PostOutModel
from services.feed_service import FeedService, get_feed_service
from services.post_service import PostService, get_post_service

router = APIRouter()


@router.post("/", status_code=HTTPStatus.CREATED,
             response_model=PostOutModel)
async def create_post(post_in: PostInModel,
                      post_service: PostService = Depends(get_post_service),
                      feed_service: FeedService = Depends(get_feed_service)) -> PostOutModel:
    post = await post_service.create(post_in.user_id, post_in.header, post_in.content)
    # start background celery task for feed update
    '''
    await feed_service.add(author_id=post.user_id,
                           header=post.header,
                           creation_date=post.creation_date,
                           content=post.content
                           )
    '''
    await update_feed.apply_async(args=(post.user_id, post.header, post.creation_date, post.content))
    return PostOutModel(**post.dict())


# delete post