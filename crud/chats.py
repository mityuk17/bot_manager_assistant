from models.chats import Chat
from db.schemas.chats import Chat as ChatDB
from sqlalchemy.sql import text
from sqlalchemy.ext.asyncio import AsyncSession
from db.db import engine


async def create_chat(chat: Chat):
    async with AsyncSession(engine) as session:
        chat_db = ChatDB(
            chat_id=chat.chat_id,
            excluded_users=chat.excluded_users
        )
        session.add(chat_db)
        await session.commit()


async def get_chat_by_id(chat_id: int):
    async with AsyncSession(engine) as session:
        result = await session.get(ChatDB, chat_id)
        return Chat.model_validate(result, from_attributes=True) if result else None


async def update_chat(chat: Chat):
    async with AsyncSession(engine) as session:
        await session.execute(
            text(f'''UPDATE chats SET 
                excluded_users = {chat.excluded_users}
                WHERE chat_id = {chat.chat_id}''')
        )
        await session.commit()


async def delete_chat(chat_id: int):
    async with AsyncSession(engine) as session:
        await session.execute(
            text(f'''DELETE FROM chats WHERE chat_id = {chat_id}''')
        )
        await session.commit()


async def get_all_chats():
    async with AsyncSession(engine) as session:
        query = await session.execute(text("SELECT * FROM chats"))
        result = query.all()
        return [Chat.model_validate(chat, from_attributes=True) for chat in result]
