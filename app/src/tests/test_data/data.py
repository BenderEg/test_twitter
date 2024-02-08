from http import HTTPStatus

user_create_parameters = [
    (
        {"data": {"name": "User"}},
        {"status": HTTPStatus.CREATED}
    ),
    (
        {"data": {}},
        {"status": HTTPStatus.CREATED}
    ),
    (
        {"data": None},
        {"status": HTTPStatus.UNPROCESSABLE_ENTITY}
    ),
]

post_create_parameters = [
    (
        {"content": {"header": "short header"}},
        {"status": HTTPStatus.CREATED}
    ),
    (
        {"content": {"header": "short header",
                     "content": "twit with content"}},
        {"status": HTTPStatus.CREATED}
    ),
    (
        {"content": {"header": 141*"a"}},
        {"status": HTTPStatus.UNPROCESSABLE_ENTITY}
    )
]