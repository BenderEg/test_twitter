from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends

from models.pagination import Pagination
from models.posts import FeedPostModel, PostOutModel
from models.read import ReadQuery, ReadFilterQuery
from models.subscriptions import SubscriptionShortModel
from models.users import UserInModel, UserOutModel
from services.feed_service import FeedService, get_feed_service
from services.post_service import PostService, get_post_service
from services.subscription_service import SubscriptionService, get_subscription_service
from services.user_service import UserService, get_user_service

router = APIRouter()


@router.post("/",
             status_code=HTTPStatus.CREATED,
             description="Создание пользователя",
             summary="Создать пользователя",
             response_model=UserOutModel
             )
async def create_user(user_in: UserInModel,
                      user_service: UserService = Depends(get_user_service)) -> UserOutModel:
    user = await user_service.create(user_in.name)
    return UserOutModel(**user.dict())


@router.get("/{user_id}/subscriptions/",
            status_code=HTTPStatus.OK,
            description="Получение подписчиков пользователя",
            summary="Получить подписчиков пользователя",
            response_model=list[SubscriptionShortModel]
            )
async def get_user_subscribers(user_id: UUID,
                               pagination: Pagination = Depends(),
                               subscription_service: SubscriptionService = Depends(
                                    get_subscription_service)) -> list[SubscriptionShortModel]:
    subscribers = await subscription_service.get_subscribers(user_id, pagination.limit, pagination.offset)
    return [SubscriptionShortModel(**ele.dict()) for ele in subscribers]


@router.get("/{user_id}/feed/",
            status_code=HTTPStatus.OK,
            description="Получение ленты пользователя",
            summary="Получить ленту пользователя",
            response_model=list[FeedPostModel]
            )
async def get_user_feed(user_id: UUID,
                        pagination: Pagination = Depends(),
                        status: ReadFilterQuery = Depends(),
                        feed_service: FeedService = Depends(
                            get_feed_service)) -> list[FeedPostModel]:
    posts = await feed_service.get_feed(user_id, pagination.limit, pagination.offset, status.read)
    return [FeedPostModel(**ele.dict()) for ele in posts]


@router.get("/{user_id}/posts/",
            status_code=HTTPStatus.OK,
            description="Получение постов пользователя",
            summary="Получить посты пользователя",
            response_model=list[PostOutModel]
            )
async def get_user_posts(user_id: UUID,
                         pagination: Pagination = Depends(),
                         post_service: PostService = Depends(
                            get_post_service)) -> list[PostOutModel]:
    posts = await post_service.get_posts(user_id, pagination.limit, pagination.offset)
    return [PostOutModel(**ele.dict()) for ele in posts]


@router.patch("/posts/{feed_id}/",
              status_code=HTTPStatus.OK,
              description="Пометка поста прочитанным",
              summary="Пометить пост прочитанным",
              response_model=FeedPostModel
              )
async def edit_feed(feed_id: UUID,
                    status: ReadQuery = Depends(),
                    feed_service: FeedService = Depends(
                        get_feed_service)) -> FeedPostModel:
    post = await feed_service.change_ridden_status(feed_id, status.read)
    return FeedPostModel(**post.dict())