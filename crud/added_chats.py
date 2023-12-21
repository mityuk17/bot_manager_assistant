from models.added_chats import AddedChats
from db.schemas.added_chats import AddedChats as AddedChatsDB
from sqlalchemy.sql import text
from sqlalchemy.ext.asyncio import AsyncSession
from db.db import engine


async def add_new_chat(chat: AddedChats):
    async with AsyncSession(engine) as session:
        chat_db = AddedChatsDB(
            chat_id=chat.chat_id,
            title=chat.title
        )
        session.add(chat_db)
        await session.commit()


async def get_chat_by_title(chat_title: str):
    async with AsyncSession(engine) as session:
        query = await session.execute(text("SELECT * FROM added_chats WHERE title=?", chat_title))
        result = query.all()
        return AddedChats.model_validate(result[0], from_attributes=True) if result else None
