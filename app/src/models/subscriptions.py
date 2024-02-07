from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, model_validator

from errors.base import SelfSubscription


class SubscriptionInModel(BaseModel):

    user_id: UUID
    subscriber_id: UUID

    @model_validator(mode="after")
    def check_ids(self) -> 'SubscriptionInModel':
        if self.user_id == self.subscriber_id:
            raise SelfSubscription
        return self


class SubscriptionOutModel(SubscriptionInModel):

    id: UUID
    creation_date: datetime


class SubscriptionShortModel(BaseModel):

    id: UUID
    user_id: UUID