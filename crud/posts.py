from models.posts import Posts
from db.schemas.posts import Posts as PostsDB
from sqlalchemy.sql import text
from sqlalchemy.ext.asyncio import AsyncSession
from db.db import engine
from datetime import datetime


async def create_post(post: Posts):
    async with AsyncSession(engine) as session:
        new_post = PostsDB(
            user_id=post.user_id,
            chat_id=post.chat_id,
            time_type=post.time_type,
            sent_time=post.sent_time,
        )
        session.add(new_post)
        await session.commit()


async def get_post_by_id(post_id: int):
    async with AsyncSession(engine) as session:
        result = await session.get(PostsDB, post_id)
        return Posts.model_validate(result, from_attributes=True) if result else None


async def update_post(post: Posts):
    async with AsyncSession(engine) as session:
        await session.execute(
            text(
                f"""UPDATE posts SET
                user_id = {post.user_id},
                chat_id = {post.chat_id}, 
                time_type = '{post.time_type}',
                sent_time = {post.sent_time}
                WHERE id = {post.id};"""
            )
        )
        await session.commit()


async def delete_post(post_id: int):
    async with AsyncSession(engine) as session:
        await session.execute(
            text(
                f"""DELETE FROM posts WHERE id = {post_id}"""
            )
        )

        await session.commit()


async def get_all_posts():
    async with AsyncSession(engine) as session:
        query = await session.execute(
            text(
                """SELECT * FROM posts"""
            )
        )

        result = query.all()
        return [Posts.model_validate(posts, from_attributes=True) for posts in result]


async def check_send_information(user_id: int, chat_id: int, time_type: str):
    async with AsyncSession(engine) as session:
        today = datetime.today().date()
        today = datetime(today.year, today.month, today.day, )
        query = await session.execute(
            text(
                f"""SELECT * FROM posts WHERE
                user_id = {user_id} AND chat_id = {chat_id}
                AND time_type = '{time_type}';"""
            )
        )
        result = query.all()
        return bool([Posts.model_validate(post, from_attributes=True) for post in result if post.sent_time > today])


async def check_send_information_for_day(user_id: int, chat_id: int, time_type: str, date_1: datetime, date_2: datetime):
    async with AsyncSession(engine) as session:
        query = await session.execute(
            text(
                f"""SELECT * FROM posts WHERE
                user_id = {user_id} AND chat_id = {chat_id}
                AND time_type = '{time_type}' AND '{date_1}' < sent_time AND '{date_2}' > sent_time;"""
            )
        )
        result = query.all()
        return bool(result)