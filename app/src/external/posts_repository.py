from uuid import UUID

from fastapi import Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from db.sqlalcem import get_session
from db.schemas import Post
from errors.base import PostWrongUser


class PostRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(
        self,
        user_id: UUID,
        header: str,
        content: str | None,
    ) -> Post:
        post = Post(user_id=user_id, header=header, content=content)
        try:
            self.session.add(post)
            await self.session.commit()
            await self.session.refresh(post)
            return post
        except IntegrityError:
            raise PostWrongUser


def get_post_repository(session: AsyncSession = Depends(get_session)) -> PostRepository:
    return PostRepository(session=session)
