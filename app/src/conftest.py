from uuid import UUID

import pytest_asyncio

from aiohttp import ClientSession

from core.config import settings
from db.sqlalcem import async_session
from tests.utils import delete_user


@pytest_asyncio.fixture(scope="module")
def make_get_request() -> tuple[dict, int]:
    async def inner(
        sub_url: str,
        headers: dict | None = None,
        query: dict | None = None,
        cookies: dict | None = None,
    ):
        async with ClientSession(base_url=settings.base_url) as session:
            async with session.get(sub_url,
                                        headers=headers,
                                        cookies=cookies,
                                        params=query
                                        ) as response:
                body = await response.json()
                status = response.status
                return body, status
    return inner


@pytest_asyncio.fixture(scope="module")
def make_post_request():
    async def inner(
        sub_url: str,
        data: dict | None = None,
        headers: dict | None = {"Content-type": "application/json"},
        cookies: dict | None = None,
    ) -> tuple[dict, int]:
        async with ClientSession(base_url=settings.base_url) as session:
            async with session.post(sub_url,
                                    headers=headers,
                                    cookies=cookies,
                                    json=data
                                    ) as response:
                body = await response.json()
                status = response.status
                return body, status
    return inner


@pytest_asyncio.fixture(scope="module")
async def get_created_user_id(make_post_request) -> UUID:
    body, _  = await make_post_request("/api/v1/users/",
                                        data={})
    user_id = body.get("id")
    yield user_id
    async with async_session() as session:
        await delete_user(user_id, session)


@pytest_asyncio.fixture(scope="module")
async def get_created_user_pair(make_post_request) -> UUID:
    body, _  = await make_post_request("/api/v1/users/",
                                        data={})
    user_id = body.get("id")
    body, _  = await make_post_request("/api/v1/users/",
                                        data={})
    subscriber_id = body.get("id")
    yield user_id, subscriber_id
    async with async_session() as session:
        await delete_user(user_id, session)
        await delete_user(subscriber_id, session)


@pytest_asyncio.fixture(scope="module")
async def get_created_user_pair_with_post(make_post_request) -> UUID:
    body, _  = await make_post_request("/api/v1/users/",
                                        data={})
    user_id = body.get("id")
    _, _  = await make_post_request("/api/v1/posts/",
                                        data={"user_id": user_id,
                                              "header": "some header"})
    body, _  = await make_post_request("/api/v1/users/",
                                        data={})
    subscriber_id = body.get("id")
    await make_post_request("/api/v1/subscriptions/",
                            data={"user_id": str(user_id),
                                    "subscriber_id": str(subscriber_id)}
                            )
    yield user_id, subscriber_id
    async with async_session() as session:
        await delete_user(user_id, session)
        await delete_user(subscriber_id, session)