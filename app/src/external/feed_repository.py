from datetime import datetime
from uuid import UUID

from fastapi import Depends
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from db.sqlalcem import get_session
from db.schemas import Post, Feed
from external.subscriptions_repository import SubscriptionRepository


class FeedRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.subscription_repo = SubscriptionRepository(session)

    async def add(
        self,
        author_id: UUID,
        header: str,
        creation_date: datetime,
        content: str | None,
    ) -> Post:
        subscribers = await self.subscription_repo.get_list(author_id, limit=None, offset=0)
        await self.session.execute(insert(Feed), [{"user_id": ele.subscriber_id,
                                                   "author_id": author_id,
                                                    "header": header,
                                                    "creation_date": creation_date,
                                                    "content": content
                                                   } for ele in subscribers]
                                )
        await self.session.commit()

    async def get_list(self, user_id: UUID, limit: int, offset: int) -> list[Feed]:
        result = await self.session.execute(select(Feed).where(Feed.user_id==user_id).limit(limit).offset(offset))
        return result.scalars().all()


def get_feed_repository(session: AsyncSession = Depends(get_session)) -> FeedRepository:
    return FeedRepository(session=session)
