from uuid import UUID
from typing import Iterable

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.sqlalcem import get_session
from db.schemas import User

class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(
        self,
        name: str | None
    ) -> User:
        user = User(name=name)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get_users_id_in_partitions(self, last_processed: UUID | None = None) -> Iterable:
        query = select(User.id)
        if last_processed:
            query = query.where(User.id > last_processed)
        query = query.order_by(User.id)
        result = await self.session.execute(query)
        users_id = result.scalars().partitions(100)
        return users_id


def get_user_repository(session: AsyncSession = Depends(get_session)) -> UserRepository:
    return UserRepository(session=session)
