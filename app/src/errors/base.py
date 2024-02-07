from http import HTTPStatus
from typing import Any

class BaseError(Exception):
    status_code: int
    detail: dict[str, Any]


class SelfSubscription(BaseError):
    status_code = HTTPStatus.FORBIDDEN
    detail = {"message": "Can not subscribe to yourself"}


class SubscriptionAlreadyExist(BaseError):
    status_code = HTTPStatus.BAD_REQUEST
    detail = {"message": "Subscription already exists"}


class SubscriptionNotFound(BaseError):
    status_code = HTTPStatus.NOT_FOUND
    detail = {"message": "Subscription not found"}


class PostWrongUser(BaseError):
    status_code = HTTPStatus.BAD_REQUEST
    detail = {"message": "Unexisting user tried to create post"}


class PostNotFound(BaseError):
    status_code = HTTPStatus.NOT_FOUND
    detail = {"message": "Post not found"}