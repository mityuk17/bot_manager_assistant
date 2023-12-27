from models.added_chats import AddedChats
from db.schemas.added_chats import AddedChats as AddedChatsDB
from sqlalchemy.sql import text
from sqlalchemy.ext.asyncio import AsyncSession
from db.db import engine


async def add_new_chat(chat: AddedChats):
    async with AsyncSession(engine) as session:
        if chat in await get_all_chats():
            return None
        chat_db = AddedChatsDB(
            chat_id=chat.chat_id,
            title=chat.title
        )
        session.add(chat_db)
        await session.commit()


async def get_chat_by_title(chat_title: str):
    async with AsyncSession(engine) as session:
        query = await session.execute(
            text(f"""SELECT * FROM added_chats WHERE title='{chat_title}';""")
        )
        result = query.all()
        return AddedChats.model_validate(result[-1], from_attributes=True) if result else None


async def get_all_chats():
    async with AsyncSession(engine) as session:
        query = await session.execute(
            text(
                """SELECT * FROM added_chats;"""
            )
        )
        result = query.all()
        return [AddedChats.model_validate(chat, from_attributes=True) for chat in result]
