from datetime import datetime
from uuid import UUID

from fastapi import Depends
from sqlalchemy import insert, select, delete, and_
from sqlalchemy.ext.asyncio import AsyncSession

from db.sqlalcem import get_session
from db.schemas import Post, Feed
from external.posts_repository import PostRepository
from external.subscriptions_repository import SubscriptionRepository


class FeedRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.subscription_repo = SubscriptionRepository(session)
        self.post_repo = PostRepository(session)

    async def add(
        self,
        author_id: UUID,
        post_id: UUID,
        header: str,
        creation_date: datetime,
        content: str | None,
    ) -> None:
        subscribers = await self.subscription_repo.get_list(author_id, limit=None, offset=0)
        await self.session.execute(insert(Feed), [{"user_id": ele.subscriber_id,
                                                   "author_id": author_id,
                                                   "post_id": post_id,
                                                   "header": header,
                                                   "creation_date": creation_date,
                                                   "content": content
                                                   } for ele in subscribers]
                                )
        await self.session.commit()

    async def get_list(self, user_id: UUID, limit: int, offset: int) -> list[Feed]:
        result = await self.session.execute(select(Feed).where(Feed.user_id==user_id).limit(limit).offset(offset))
        return result.scalars().all()

    async def delete(self, author_id: UUID, post_id: UUID) -> None:
        subscribers = await self.subscription_repo.get_list(author_id, limit=None, offset=0)
        subscribers_ids = [ele.subscriber_id for ele in subscribers]
        await self.session.execute(delete(Feed).where(and_(Feed.user_id.in_(subscribers_ids),
                                                      Feed.post_id==post_id))
                                                      )
        await self.session.commit()

    async def add_posts(self, author_id: UUID, subscriber_id: UUID) -> None:
        posts = await self.post_repo.get_list(author_id, limit=None, offset=0)
        await self.session.execute(insert(Feed), [{"user_id": subscriber_id,
                                                   "author_id": author_id,
                                                   "post_id": ele.id,
                                                   "header": ele.header,
                                                   "creation_date": ele.creation_date,
                                                   "content": ele.content
                                                   } for ele in posts]
                                    )
        await self.session.commit()

    async def delete_feeds_by_author_id(self, author_id: UUID, subscriber_id: UUID) -> None:
        await self.session.execute(delete(Feed).where(and_(Feed.user_id==subscriber_id,
                                                      Feed.author_id==author_id))
                                                      )
        await self.session.commit()

def get_feed_repository(session: AsyncSession = Depends(get_session)) -> FeedRepository:
    return FeedRepository(session=session)
