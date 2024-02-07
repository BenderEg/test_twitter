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

        result = await self.post_repository.create(user_id, header, content)
        return result

    async def delete(self, post_id: UUID) -> bool:
        """Delete post."""

        result = await self.post_repository.delete(post_id)
        return result


def get_post_service(
    post_repository: PostRepository = Depends(get_post_repository),
) -> PostService:
    return PostService(
        post_repository=post_repository
        )