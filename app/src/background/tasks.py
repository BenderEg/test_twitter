from datetime import datetime
from uuid import UUID

from services.feed_service import FeedService

async def add_new_posts_to_feed(author_id: UUID,
                                post_id: UUID,
                                header: str,
                                creation_date: datetime,
                                content: str | None,
                                service: FeedService
                                ):
    await service.add(author_id, post_id, header, creation_date, content)


async def delete_posts_from_feed(author_id: UUID,
                                 post_id: UUID,
                                 service: FeedService
                                 ):
    await service.delete_posts(author_id, post_id)


async def add_posts_for_new_subscriber(author_id: UUID,
                                       subscriber_id: UUID,
                                       service: FeedService
                                       ):
    await service.add_posts_for_new_subscriber(author_id, subscriber_id)


async def delete_posts_by_author_id(author_id: UUID,
                                    subscriber_id: UUID,
                                    service: FeedService
                                    ):
    await service.delete_posts_for_author(author_id, subscriber_id)