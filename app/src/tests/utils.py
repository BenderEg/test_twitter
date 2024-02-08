from uuid import UUID

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from db.schemas import User


async def delete_user(user_id: UUID, session: AsyncSession):
    await session.execute(delete(User).where(User.id==user_id))