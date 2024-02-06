from http import HTTPStatus
from typing import Any

class BaseError(Exception):
    status_code: int
    detail: dict[str, Any]


class SelfSubscriptionError(BaseError):
    status_code = HTTPStatus.FORBIDDEN
    detail = {"message": "Can not subscribe to yourself"}


class SubscriptionAlreadyExistError(BaseError):
    status_code = HTTPStatus.FORBIDDEN
    detail = {"message": "Subscription already exists"}