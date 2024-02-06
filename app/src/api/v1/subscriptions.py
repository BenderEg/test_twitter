from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, Response

from models.subscriptions import SubscriptionInModel, SubscriptionOutModel
from services.feed_service import FeedService, get_feed_service
from services.subscription_service import SubscriptionService, get_subscription_service

router = APIRouter()


@router.post("/", status_code=HTTPStatus.CREATED,
                  response_model=SubscriptionOutModel)
async def add_subscription(subscription_in: SubscriptionInModel,
                           subscription_service: SubscriptionService = Depends(
                               get_subscription_service),
                           feed_service: FeedService = Depends(
                               get_feed_service)) -> SubscriptionOutModel:
    subscription = await subscription_service.create(
        subscription_in.user_id,
        subscription_in.subscriber_id
        )
    # start background celery task for feed update
    return SubscriptionOutModel(**subscription.dict())


@router.delete("/{subscription_id}/", status_code=HTTPStatus.OK,
                  response_class=Response)
async def delete_subscription(subscription_id: UUID,
                              subscription_service: SubscriptionService = Depends(
                                  get_subscription_service)
                                  ) -> Response:
    await subscription_service.delete(subscription_id)
    # start background celery task for feed update
    return Response(status_code=HTTPStatus.OK)