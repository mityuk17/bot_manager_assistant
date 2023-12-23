from models.newsletters import Newsletters
from db.schemas.newsletters import Newsletters as NewslettersDB
from sqlalchemy.sql import text
from sqlalchemy.ext.asyncio import AsyncSession
from db.db import engine


async def create_newsletter(newsletter: Newsletters):
    async with AsyncSession(engine) as session:
        newsletter_db = NewslettersDB(
            message_id=newsletter.message_id,
            user_id=newsletter.user_id,
            chat_id=newsletter.chat_id,
            time=newsletter.time,
            week_days=newsletter.week_days,
        )
        session.add(newsletter_db)
        await session.commit()


async def get_newsletter_by_id(newsletter_id: int):
    async with AsyncSession(engine) as session:
        result = await session.get(NewslettersDB, newsletter_id)
        return Newsletters.model_validate(result, from_attributes=True) if result else None


async def update_newsletters(newsletter: Newsletters):
    async with AsyncSession(engine) as session:
        # В time возможно тоже кавычки должны быть
        await session.execute(
            text(
                f"""UPDATE newsletters SET
                message_id = {newsletter.message_id},
                user_id = {newsletter.user_id}, 
                chat_id = {newsletter.chat_id},
                time = {newsletter.time}, 
                week_days = "{newsletter.week_days}" 
                WHERE id = {newsletter.id};"""
            )
        )
        await session.commit()


async def delete_newsletters(newsletter_id: int):
    async with AsyncSession(engine) as session:
        await session.execute(
            text(
                f'''DELETE FROM newsletters WHERE id = {newsletter_id};'''
            )
        )

        await session.commit()


async def get_all_newsletters():
    async with AsyncSession(engine) as session:
        query = await session.execute(text("SELECT * FROM newsletters;"))
        result = query.all()
        return [Newsletters.model_validate(newsletter, from_attributes=True) for newsletter in result]
