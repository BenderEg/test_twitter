from fastapi import Depends
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


def get_user_repository(session: AsyncSession = Depends(get_session)) -> UserRepository:
    return UserRepository(session=session)
