from uuid import UUID

from fastapi import Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from db.sqlalcem import get_session
from db.schemas import Subscription
from errors.base import SubscriptionAlreadyExistError

class SubscriptionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(
        self,
        user_id: UUID,
        subscriber_id: UUID,
    ) -> Subscription:
        try:
            subscription = Subscription(user_id=user_id, subscriber_id=subscriber_id)
            self.session.add(subscription)
            await self.session.commit()
            await self.session.refresh(subscription)
            return subscription
        except IntegrityError:
            raise SubscriptionAlreadyExistError


def get_subscription_repository(session: AsyncSession = Depends(get_session)) -> SubscriptionRepository:
    return SubscriptionRepository(session=session)
