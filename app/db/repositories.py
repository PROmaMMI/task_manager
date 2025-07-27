from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models import UserORM
from app.domain.user import User

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: int) -> User | None:
        stmt = select(UserORM).where(UserORM.id == user_id)
        result = await self.session.execute(stmt)
        orm_user = result.scalar_one_or_none()
        if orm_user:
            return User(id=orm_user.id, username=orm_user.username, email=orm_user.email)
        return None
