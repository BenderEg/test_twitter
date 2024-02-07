from datetime import datetime
from typing import Iterable
from uuid import UUID

from fastapi import Depends
from sqlalchemy import insert, select, delete, and_, update, desc, text, bindparam
from sqlalchemy.ext.asyncio import AsyncSession

from db.sqlalcem import get_session
from db.schemas import Feed
from external.posts_repository import PostRepository
from external.subscriptions_repository import SubscriptionRepository
from external.user_repository import UserRepository

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

    async def get_list(self, user_id: UUID, limit: int, offset: int, status: bool | None = None) -> list[Feed]:
        stmt = select(Feed).where(Feed.user_id==user_id)
        if status is not None:
            stmt = stmt.where(Feed.read==status)
        result = await self.session.execute(stmt.limit(limit).offset(offset).order_by(desc(Feed.creation_date)))
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

    async def change_ridden_status(self, feed_id: UUID, status: bool) -> Feed:
        result = await self.session.execute(update(Feed).where(Feed.id==feed_id).values({"read": status}).returning(Feed))
        feed = result.scalar_one()
        await self.session.commit()
        return feed

    async def get_feeds(self, users_id: UUID, twit_numbers: int):
        query = text(f'''WITH tab1 AS (
                SELECT
                    *,
                    ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY creation_date DESC) AS row_num
                FROM feeds
                WHERE user_id IN :users
            )
            SELECT tab1.user_id,  ARRAY_AGG((tab1.author_id,
                                            tab1.header,
                                            tab1.content,
                                            tab1.creation_date)) AS row_values
            FROM tab1
            WHERE row_num <= :twit_number
            group by tab1.user_id''')
        query = query.bindparams(bindparam("users", expanding=True),
                                 bindparam("twit_number"),
                                 users=users_id,
                                 twit_number=twit_numbers)
        result = await self.session.execute(query)
        return result.fetchall()

    async def clean_feeds_table(self, max_twits: int):
        stmt = text(f'''DELETE FROM feeds
WHERE id IN (
    SELECT id
    FROM (
        SELECT id,
            ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY creation_date DESC) AS row_num
        FROM feeds
    ) AS subquery
    WHERE subquery.row_num > :max_twits)''')
        stmt = stmt.bindparams(bindparam("max_twits"),
                               max_twits=max_twits)
        await self.session.execute(stmt)
        await self.session.commit()

def get_feed_repository(session: AsyncSession = Depends(get_session)) -> FeedRepository:
    return FeedRepository(session=session)