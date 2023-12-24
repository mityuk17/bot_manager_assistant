from models.users import User
from db.schemas.users import User as UserDB
from sqlalchemy.sql import text
from sqlalchemy.ext.asyncio import AsyncSession
from db.db import engine


async def create_user(user: User):
    async with AsyncSession(engine) as session:
        user_db = UserDB(
            user_id=user.user_id,
            chat_id=user.chat_id,
            fullname=user.fullname,
            town=user.town,
            time_start=user.time_start,
            time_end=user.time_end,
            week_days=user.week_days,
            job_title=user.job_title,
            product=user.product,
            metrics=user.metrics
        )
        session.add(user_db)
        await session.commit()


async def get_user_by_user_id_and_chat_id(user_id: int, chat_id: str):
    async with AsyncSession(engine) as session:
        result = await session.get(UserDB, [user_id, chat_id])
        return User.model_validate(result, from_attributes=True) if result else None


async def update_user_by_user_id_and_chat_id(user: User):
    async with AsyncSession(engine) as session:
        await session.execute(
            text(
                f"""UPDATE "users" SET
                fullname = "{user.fullname}",
                town = "{user.town}",
                time_start = {user.time_start}, 
                time_end = {user.time_end},
                week_days = "{user.week_days}",
                job_title = "{user.job_title}", 
                product = "{user.product}",
                metrics = "{user.metrics}"
                WHERE user_id = {user.user_id} AND chat_id = {user.chat_id};"""
            )
        )

        await session.commit()


async def delete_user_by_user_id_and_chat_id(user: User):
    async with AsyncSession(engine) as session:
        await session.execute(
            text(
                f"""DELETE FROM 'users'
                WHERE user_id = {user.user_id} AND chat_id = '{user.chat_id}';"""
            )
        )

        await session.commit()


async def get_all_users():
    async with AsyncSession(engine) as session:
        query = await session.execute(
            text(
                """SELECT * FROM 'users';"""
            )
        )
        result = query.all()
        return [User.model_validate(users, from_attributes=True) for users in result]
