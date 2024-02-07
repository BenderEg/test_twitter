from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, Response, BackgroundTasks

from background.tasks import add_posts_for_new_subscriber, delete_posts_by_author_id
from models.subscriptions import SubscriptionInModel, SubscriptionOutModel
from services.feed_service import FeedService, get_feed_service
from services.subscription_service import SubscriptionService, get_subscription_service

router = APIRouter()


@router.post("/", status_code=HTTPStatus.CREATED,
                  response_model=SubscriptionOutModel)
async def add_subscription(subscription_in: SubscriptionInModel,
                           background_tasks: BackgroundTasks,
                           subscription_service: SubscriptionService = Depends(
                               get_subscription_service),
                           feed_service: FeedService = Depends(
                               get_feed_service)) -> SubscriptionOutModel:
    subscription = await subscription_service.create(
        subscription_in.user_id,
        subscription_in.subscriber_id
        )
    background_tasks.add_task(add_posts_for_new_subscriber, subscription.user_id,
                              subscription.subscriber_id, feed_service)
    return SubscriptionOutModel(**subscription.dict())


@router.delete("/{subscription_id}/", status_code=HTTPStatus.OK,
                  response_class=Response)
async def delete_subscription(subscription_id: UUID,
                              background_tasks: BackgroundTasks,
                              subscription_service: SubscriptionService = Depends(
                                  get_subscription_service),
                              feed_service: FeedService = Depends(
                               get_feed_service)
                                  ) -> Response:
    deleted_subscription = await subscription_service.delete(subscription_id)
    background_tasks.add_task(delete_posts_by_author_id, deleted_subscription.user_id,
                              deleted_subscription.subscriber_id, feed_service)
    return Response(status_code=HTTPStatus.OK)