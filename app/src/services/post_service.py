from uuid import UUID

from fastapi import Depends

from db.schemas import Post
from external.posts_repository import PostRepository, get_post_repository


class PostService:
    def __init__(
        self,
        post_repository: PostRepository
    ) -> None:
        self.post_repository = post_repository


    async def create(self, user_id: UUID, header: str, content: str | None) -> Post:
        """Create new post."""

        return await self.post_repository.create(user_id, header, content)

    async def delete(self, post_id: UUID) -> bool:
        """Delete post."""

        return await self.post_repository.delete(post_id)

    async def get_posts(self, user_id: UUID, limit: int, offset: int) -> list[Post]:
        """Get users posts."""

        return await self.post_repository.get_list(user_id, limit, offset)


def get_post_service(
    post_repository: PostRepository = Depends(get_post_repository),
) -> PostService:
    return PostService(
        post_repository=post_repository
        )