from fastapi import Depends

from db.schemas import User
from external.user_repository import UserRepository, get_user_repository


class UserService:
    def __init__(
        self,
        user_repository: UserRepository
    ) -> None:
        self.user_repository = user_repository


    async def create(self, name: str | None) -> User:
        """Create new user."""

        result = await self.user_repository.create(name)
        return result


def get_user_service(
    user_repository: UserRepository = Depends(get_user_repository),
) -> UserService:
    return UserService(
        user_repository=user_repository
        )