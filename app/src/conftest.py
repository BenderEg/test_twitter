from uuid import UUID

import pytest_asyncio

from aiohttp import ClientSession


@pytest_asyncio.fixture
def make_get_request() -> tuple[dict, int]:
    async def inner(
        sub_url: str,
        headers: dict | None = None,
        query: dict | None = None,
        cookies: dict | None = None,
    ):
        async with ClientSession(base_url="http://localhost:8000") as session:
            async with session.get(sub_url,
                                        headers=headers,
                                        cookies=cookies,
                                        params=query
                                        ) as response:
                return response.json(), response.status_code
    return inner


@pytest_asyncio.fixture
def make_post_request():
    async def inner(
        sub_url: str,
        data: dict | None = None,
        headers: dict | None = {"Content-type": "application/json"},
        cookies: dict | None = None,
    ) -> tuple[dict, int]:
        async with ClientSession(base_url="http://localhost:8000") as session:
            async with session.post(sub_url,
                                    headers=headers,
                                    cookies=cookies,
                                    json=data
                                    ) as response:
                body = await response.json()
                status = response.status
                return body, status
    return inner


@pytest_asyncio.fixture
async def get_created_user_id(make_post_request) -> UUID:
    body, _  = await make_post_request("/api/v1/users/",
                                        data={})
    return body.get("id")