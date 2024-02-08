from copy import copy
from random import choices, randint
from string import ascii_letters, ascii_uppercase, punctuation, digits
from uuid import UUID, uuid4

import asyncio

from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from external.posts_repository import get_post_repository
from external.subscriptions_repository import get_subscription_repository
from db.schemas import User, Subscription, Post, Feed
from db.sqlalcem import async_session


SYMBOLS = ascii_letters + ascii_uppercase + punctuation + digits


def generate_users_id(number: int) -> list[UUID]:
    return [uuid4() for _ in range(number)]

async def create_users(users_id: list[UUID], session: AsyncSession) -> None:

    await session.execute(insert(User).values([{"id": ele} for ele in users_id]))
    await session.commit()

async def create_subscriptions(users_id: list[UUID], session: AsyncSession) -> None:
    for ele in users_id:
        ids_copy = copy(users_id)
        ids_copy.remove(ele)
        await session.execute(insert(Subscription).values([{"user_id": ele,
                                                            "subscriber_id": value} for value in ids_copy]))
    await session.commit()

async def create_posts(users_id: list[UUID], session: AsyncSession) -> None:
    for ele in users_id:
        await session.execute(insert(Post).values(
            [{"user_id": ele,
            "header": "".join(choices(SYMBOLS, k=randint(1, 140)))
            } for _ in range(500)]))
    await session.commit()

async def create_feeds(users_id: list[UUID], session: AsyncSession) -> None:
    subs_repo = get_subscription_repository(session)
    post_repo = get_post_repository(session)
    for ele in users_id:
        subscribers = await subs_repo.get_list(ele, limit=None, offset=0)
        posts = await post_repo.get_list(ele, limit=None, offset=0)
        for subscriber in subscribers:
            await session.execute(insert(Feed).values(
                [{"user_id": subscriber.subscriber_id,
                  "author_id": ele,
                  "post_id": post.id,
                  "header": post.header,
                  "content": post.content,
                  "creation_date": post.creation_date,
                  "read": False} for post in posts])
                  )
    await session.commit()


async def create_data(number: int) -> None:
    users_id = generate_users_id(number)
    async with async_session() as session:
        for i in range(0, len(users_id), 100):
            await create_users(users_id[i: i+100], session)
        for i in range(0, len(users_id), 100):
            await create_subscriptions(users_id[i: i+100], session)
        for i in range(0, len(users_id), 100):
            await create_posts(users_id[i: i+100], session)
        for i in range(0, len(users_id), 100):
            await create_feeds(users_id[i: i+100], session)


if __name__ == "__main__":
    asyncio.run(create_data(100))