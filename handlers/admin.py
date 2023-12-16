from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()


@router.message(Command('admin'))
async def hello_world(message: Message):
    await message.answer(f'Hello, admin - {message.from_user.first_name}!')


