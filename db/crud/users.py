from db.schemas import User as UserDB
from db.models import User as User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db.db import engine


async def create_user(user: User):
    async with AsyncSession(engine) as session:
        user_db = UserDB(**user.model_dump())
        session.add(user_db)
        await session.commit()
        await session.refresh(user_db)


async def read_user(peer_id: int):
    async with AsyncSession(engine) as session:
        query = await session.execute(
            select(UserDB).where(UserDB.peer_id == peer_id)
        )
        result = query.scalars().first()
        return result


async def get_users():
    async with AsyncSession(engine) as session:
        query = await session.execute(
            select(UserDB)
        )
        return [user.peer_id for user in query.scalars().all()]


async def change_user_status(peer_id: int, status: bool):
    async with AsyncSession(engine) as session:
        query = await session.execute(
            select(UserDB).where(UserDB.peer_id == peer_id)
        )
        user = query.scalar_one()
        user.ref_status = status
        await session.commit()
