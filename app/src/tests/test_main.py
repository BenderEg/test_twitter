from http import HTTPStatus

import pytest

from tests.test_data.data import user_create_parameters, post_create_parameters

@pytest.mark.parametrize("data, expected_answer", user_create_parameters)
@pytest.mark.asyncio
async def test_create_user(make_post_request, data, expected_answer):
    _, status = await make_post_request("/api/v1/users/",
                                        data=data["data"])

    assert status == expected_answer["status"]


@pytest.mark.parametrize("data, expected_answer", post_create_parameters)
@pytest.mark.asyncio
async def test_create_post(get_created_user_id, make_post_request, data, expected_answer):
    user_id = get_created_user_id
    data = data["content"]
    data["user_id"] = str(user_id)
    _, status = await make_post_request("/api/v1/posts/",
                                        data=data
                                        )
    assert status == expected_answer["status"]