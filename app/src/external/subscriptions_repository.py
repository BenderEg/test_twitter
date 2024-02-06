from uuid import UUID

from fastapi import Depends
from sqlalchemy import delete
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from db.sqlalcem import get_session
from db.schemas import Subscription
from errors.base import SubscriptionAlreadyExist, SubscriptionNotFound

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
            raise SubscriptionAlreadyExist

    async def delete(self, subscription_id: UUID) -> bool:
        result = await self.session.execute(
            delete(Subscription).where(Subscription.id == subscription_id).returning(Subscription.id),
        )
        try:
            _ = result.scalar_one()
        except NoResultFound:
            raise SubscriptionNotFound
        await self.session.commit()
        return True


def get_subscription_repository(session: AsyncSession = Depends(get_session)) -> SubscriptionRepository:
    return SubscriptionRepository(session=session)
