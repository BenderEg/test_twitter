from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, model_validator

from errors.base import SelfSubscriptionError


class SubscriptionInModel(BaseModel):

    user_id: UUID
    subscriber_id: UUID

    @model_validator(mode="after")
    def check_ids(self) -> 'SubscriptionInModel':
        if self.user_id == self.subscriber_id:
            raise SelfSubscriptionError
        return self


class SubscriptionOutModel(SubscriptionInModel):

    id: UUID
    creation_date: datetime