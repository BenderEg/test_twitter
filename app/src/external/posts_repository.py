from uuid import UUID

from fastapi import Depends
from sqlalchemy import delete, select, desc
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from db.sqlalcem import get_session
from db.schemas import Post
from errors.base import PostNotFound, PostWrongUser


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

    async def delete(self, post_id: UUID) -> bool:
        result = await self.session.execute(
            delete(Post).where(Post.id == post_id).returning(Post.id),
        )
        try:
            _ = result.scalar_one()
        except NoResultFound:
            raise PostNotFound
        await self.session.commit()
        return True

    async def get_list(self, user_id: UUID, limit: int, offset: int) -> list[Post]:
        result = await self.session.execute(select(Post).where(
            Post.user_id==user_id).limit(limit).offset(offset).order_by(
                desc(Post.creation_date)))
        return result.scalars().all()


def get_post_repository(session: AsyncSession = Depends(get_session)) -> PostRepository:
    return PostRepository(session=session)
