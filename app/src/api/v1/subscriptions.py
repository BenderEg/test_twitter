from http import HTTPStatus

from fastapi import APIRouter, Depends

from models.subscriptions import SubscriptionInModel, SubscriptionOutModel
from services.subscription_service import SubscriptionService, get_subscription_service

router = APIRouter()


@router.post("/", status_code=HTTPStatus.CREATED,
                  response_model=SubscriptionOutModel)
async def add_subscription(subscription_in: SubscriptionInModel,
                           subscription_service: SubscriptionService = Depends(
                               get_subscription_service)) -> SubscriptionOutModel:
    subscription = await subscription_service.create(
        subscription_in.user_id,
        subscription_in.subscriber_id
        )
    return SubscriptionOutModel(**subscription.dict())