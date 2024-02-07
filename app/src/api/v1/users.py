from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends

from models.pagination import Pagination
from models.posts import FeedPostModel
from models.read import ReadQuery
from models.subscriptions import SubscriptionShortModel
from models.users import UserInModel, UserOutModel
from services.feed_service import FeedService, get_feed_service
from services.subscription_service import SubscriptionService, get_subscription_service
from services.user_service import UserService, get_user_service

router = APIRouter()


@router.post("/", status_code=HTTPStatus.CREATED,
             response_model=UserOutModel)
async def create_user(user_in: UserInModel,
                      user_service: UserService = Depends(get_user_service)) -> UserOutModel:
    user = await user_service.create(user_in.name)
    return UserOutModel(**user.dict())


@router.get("/{user_id}/subscriptions/", status_code=HTTPStatus.OK,
            response_model=list[SubscriptionShortModel])
async def get_user_subscribers(user_id: UUID,
                               pagination: Pagination = Depends(),
                               subscription_service: SubscriptionService = Depends(
                                    get_subscription_service)) -> list[SubscriptionShortModel]:
    subscribers = await subscription_service.get_subscribers(user_id, pagination.limit, pagination.offset)
    return [SubscriptionShortModel(**ele.dict()) for ele in subscribers]


@router.get("/{user_id}/posts/", status_code=HTTPStatus.OK,
            response_model=list[FeedPostModel])
async def get_user_feed(user_id: UUID,
                        pagination: Pagination = Depends(),
                        feed_service: FeedService = Depends(
                            get_feed_service)) -> list[FeedPostModel]:
    posts = await feed_service.get_feed(user_id, pagination.limit, pagination.offset)
    return [FeedPostModel(**ele.dict()) for ele in posts]


@router.patch("/posts/{feed_id}/", status_code=HTTPStatus.OK,
              response_model=FeedPostModel)
async def edit_feed(feed_id: UUID,
                    status: ReadQuery = Depends(),
                    feed_service: FeedService = Depends(
                        get_feed_service)) -> FeedPostModel:
    post = await feed_service.change_ridden_status(feed_id, status.read)
    return FeedPostModel(**post.dict())