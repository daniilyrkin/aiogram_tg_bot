from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.types.input_file import FSInputFile
from utils.logger import logger
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import orm_add

import os
from keyboards.keyboards import Keyboards_all as key


client_router = Router()


@client_router.message(Command('start', 'help', 'menu'))
async def help(message: Message, session: AsyncSession):
    username = message.from_user.username
    user_id = message.from_user.id
    await orm_add(session=session, tablename='User', data=({'id': user_id, 'username': username}))
    await message.answer(
        text=f"Приветствую {message.from_user.first_name}!\n"
        "Я БОТ, нажми на одну из кнопок для продолженияz",
        reply_markup=await key.start_key())
    await logger(message, text=message.text)


@client_router.message(Command('user_id'))
async def user_id(message: Message):
    await message.answer(f"Твой ID: {message.from_user.id}")
    await logger(message, text=message.text)


# Функция для отправки и просмотра файлов в папке
@client_router.message(Command('download'))
async def download_(message: Message):
    list_program = os.listdir('download')
    for x in list_program:
        ss = FSInputFile(f"download/{x}")
        await message.answer_document(ss)
    await logger(message, text=message.text)
