from uuid import UUID

from fastapi import Depends

from db.schemas import Subscription
from external.subscriptions_repository import SubscriptionRepository, get_subscription_repository


class SubscriptionService:
    def __init__(
        self,
        subscription_repository: SubscriptionRepository
    ) -> None:
        self.subscription_repository = subscription_repository


    async def create(self, user_id: UUID, subscriber_id: UUID) -> Subscription:
        """Create new subscription."""

        result = await self.subscription_repository.create(user_id, subscriber_id)
        return result

    async def delete(self, subscription_id: UUID) -> Subscription:
        """Delete subscription."""

        result = await self.subscription_repository.delete(subscription_id)
        return result

    async def get_subscribers(self, user_id: UUID, limit: int, offset: int) -> list[Subscription]:
        """Get user subscribers."""

        result = await self.subscription_repository.get_list(user_id, limit, offset)
        return result



def get_subscription_service(
    subscription_repository: SubscriptionRepository = Depends(get_subscription_repository),
) -> SubscriptionService:
    return SubscriptionService(
        subscription_repository=subscription_repository
        )