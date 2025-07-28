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

    async def get_all(self) -> list[User]:
        stmt = select(UserORM)
        result = await self.session.execute(stmt)
        users = result.scalars().all()
        return [User(id=u.id, username=u.username, email=u.email) for u in users]
    
    async def create(self, username: str, email: str) -> User:
        user_orm = UserORM(username=username, email=email)
        self.session.add(user_orm)
        await self.session.commit()
        await self.session.refresh(user_orm)
        return User(id=user_orm.id, username=user_orm.username, email=user_orm.email)
    
    async def update(self, user_id: int, username: str | None = None, email: str | None = None) -> User | None:
        stmt = select(UserORM).where(UserORM.id == user_id)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()
        if not user:
            return None
        if username is not None:
            user.username = username
        if email is not None:
            user.email = email
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return User(id=user.id, username=user.username, email=user.email)

    async def delete(self, user_id: int) -> bool:
        stmt = select(UserORM).where(UserORM.id == user_id)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()
        if not user:
            return False
        await self.session.delete(user)
        await self.session.commit()
        return True