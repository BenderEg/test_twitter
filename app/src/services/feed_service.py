from datetime import datetime
from uuid import UUID

from fastapi import Depends

from external.feed_repository import FeedRepository, get_feed_repository
from db.schemas import Feed

class FeedService:
    def __init__(
        self,
        feed_repository: FeedRepository
    ) -> None:
        self.feed_repository = feed_repository

    async def add(self,
                  author_id: UUID,
                  post_id: UUID,
                  header: str,
                  creation_date: datetime,
                  content: str | None
                  ) -> None:
        """Add post to subscribers feed."""

        await self.feed_repository.add(author_id, post_id, header, creation_date, content)

    async def get_feed(self, user_id: UUID, limit: int, offset: int) -> list[Feed]:
        """Get user feed."""

        result = await self.feed_repository.get_list(user_id, limit, offset)
        return result

    async def delete_posts(self, author_id: UUID, post_id: UUID) -> None:
        """Delete posts from feed for all authors subscribers."""

        await self.feed_repository.delete(author_id, post_id)

    async def add_posts_for_new_subscriber(self, author_id: UUID, subscriber_id: UUID) -> None:
        """Add all authors posts to new subscribers feed."""

        await self.feed_repository.add_posts(author_id, subscriber_id)

    async def delete_posts_for_author(self, author_id: UUID, subscriber_id: UUID) -> None:
        """Delete all authors posts from subscribers feed."""

        await self.feed_repository.delete_feeds_by_author_id(author_id, subscriber_id)


def get_feed_service(
    feed_repository: FeedService = Depends(get_feed_repository),
) -> FeedService:
    return FeedService(
        feed_repository=feed_repository
        )