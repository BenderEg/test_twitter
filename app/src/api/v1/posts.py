from http import HTTPStatus

from fastapi import APIRouter, Depends, BackgroundTasks, Response

from background.tasks import add_new_posts_to_feed, delete_posts_from_feed
from models.posts import PostInModel, PostOutModel, DeletedPostModel
from services.feed_service import FeedService, get_feed_service
from services.post_service import PostService, get_post_service

router = APIRouter()


@router.post("/",
             status_code=HTTPStatus.CREATED,
             description="Создание нового поста",
             summary="Создать новый пост",
             response_model=PostOutModel
             )
async def create_post(post_in: PostInModel,
                      background_tasks: BackgroundTasks,
                      post_service: PostService = Depends(get_post_service),
                      feed_service: FeedService = Depends(get_feed_service)) -> PostOutModel:
    post = await post_service.create(post_in.user_id, post_in.header, post_in.content)
    background_tasks.add_task(add_new_posts_to_feed, post.user_id,
                              post.id, post.header, post.creation_date,
                              post.content, feed_service)
    return PostOutModel(**post.dict())


@router.delete("/",
               status_code=HTTPStatus.OK,
               description="Удаление поста",
               summary="Удалить пост",
               response_class=Response
               )
async def delete_post(deleted_post: DeletedPostModel,
                      background_tasks: BackgroundTasks,
                      post_service: PostService = Depends(get_post_service),
                      feed_service: FeedService = Depends(get_feed_service)
                      ) -> Response:
    await post_service.delete(deleted_post.post_id)
    background_tasks.add_task(delete_posts_from_feed, deleted_post.user_id,
                              deleted_post.post_id, feed_service)
    return Response(status_code=HTTPStatus.OK)