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
                  header: str,
                  creation_date: datetime,
                  content: str | None
                  ) -> None:
        """Add post to subscribers feed."""

        result = await self.feed_repository.add(author_id, header, creation_date, content)
        return result

    async def get_feed(self, user_id: UUID, limit: int, offset: int) -> list[Feed]:
        """Get user feed."""

        result = await self.feed_repository.get_list(user_id, limit, offset)
        return result


def get_feed_service(
    feed_repository: FeedService = Depends(get_feed_repository),
) -> FeedService:
    return FeedService(
        feed_repository=feed_repository
        )