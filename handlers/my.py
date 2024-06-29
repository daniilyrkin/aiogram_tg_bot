from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, KeyboardButton, CallbackQuery, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types.input_file import FSInputFile
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from collections import deque
from sqlalchemy.ext.asyncio import AsyncSession
from database.orm_query import orm_add, orm_get, orm_get_one


import os
import datetime
from dotenv import load_dotenv

from config import bot
from state_handlers import state as st

my_router = Router()
load_dotenv()

ADMIN = int(os.getenv('ADMIN'))
my_router.message.filter(F.chat.id.in_({ADMIN}))


@my_router.message(Command('my'))
async def my_command(message: Message):
    kb = [
        [
            KeyboardButton(text='/BD'),
            KeyboardButton(text='/list_id'),
            KeyboardButton(text='/weather'),
            KeyboardButton(text='/music_yt'),
            KeyboardButton(text="/get_mail_list")
        ],
        [
            KeyboardButton(text='/logs'),
            KeyboardButton(text='/траты'),
            KeyboardButton(text='/investment'),
            KeyboardButton(text='/health'),
            KeyboardButton(text='/one-time_mail')
        ]
    ]
    key = ReplyKeyboardBuilder(kb)
    await message.answer(
        text='Привет создатель! Что делать будем?',
        reply_markup=key.as_markup(
            resize_keyboard=True,
            input_field_placeholder="Нажми что-нибудь..."))


@my_router.message(Command('investment'))
async def my_comm(message: Message):
    key = InlineKeyboardBuilder()
    key.button(text='Добавить', callback_data='add_invest')
    key.button(text='Всего вложено', callback_data='invest_all')
    key.adjust(1)
    await message.answer(
        text='Выбери комманду',
        reply_markup=key.as_markup(
            resize_keyboard=True,
            input_field_placeholder="Нажми уже что-нибудь..."))


@my_router.callback_query(F.data == 'add_invest')
async def my_comm_add(
        callback: CallbackQuery,
        state: FSMContext):
    await bot.send_message(
        chat_id=callback.from_user.id,
        text='Введи сколько вложил')
    await callback.answer(cache_time=1)
    await state.set_state(st.InvestState.Money_Up)


@my_router.message(st.InvestState.Money_Up)
async def add_money(message: Message, state: FSMContext, session: AsyncSession):
    user_msg = int(message.text)
    money_all_ = await orm_get_one(session=session, tablename='Investment')
    money_all = (user_msg + int(money_all_.all_money)) if money_all_ is not None else user_msg
    await orm_add(
        tablename='Investment',
        session=session,
        data={'amount': user_msg, 'all_money': money_all})
    await state.clear()
    money_now = await orm_get_one(session=session, tablename='Investment')
    await message.answer(text=f'Записано вложекние\nВсего вложено {money_now.all_money}₽')


@my_router.callback_query(F.data == 'invest_all')
async def invest_all(callback: CallbackQuery, session: AsyncSession):
    await callback.answer()
    money_now = await orm_get_one(session=session, tablename='Investment')
    if money_now is None:
        await callback.message.answer(text='Нет данных')
    else:
        await callback.message.answer(text=f'Всего вложено {money_now.all_money}₽')


@my_router.message(Command('BD'))
async def birthday(message: Message, session: AsyncSession):
    await bot.send_message(
        chat_id=ADMIN,
        text='Смотрим у кого сегодня или завтра день рождения...')
    day_now = int(datetime.datetime.now().strftime('%d'))
    mon_now = int(datetime.datetime.now().strftime('%m'))
    for b_d in await orm_get(session=session, tablename='Birthday'):
        if int(b_d.b_mon) == mon_now:
            if int(b_d.b_day) == day_now + 7:
                text = f'{b_d.b_day} день рождения у {b_d.name}!😃'
                break
            elif int(b_d.b_day) == day_now:
                text = f'Сегодня день рождения у {b_d.name}!😃'
                break
        else:
            text = 'Ни сегодня ни завтра день рождений не предвидется🙃'
    await bot.send_message(chat_id=ADMIN, text=text)


@my_router.message(Command('list_id'))
async def list_id(message: Message, session: AsyncSession):
    text = ''
    for user in await orm_get(session=session, tablename='User'):
        if id:
            text += f'ID: {user.id}, Имя: {user.username}\n'
        else:
            text = 'Пользователи не найдены'
    await message.answer(text)


@my_router.message(Command('logs'))
async def logs(message: Message):
    text = ''
    with open('bot.txt', 'r') as file:
        lines = deque(file, maxlen=10)
        for line in lines:
            text += f'{line}\n'
    ss = FSInputFile("bot.txt")
    await message.answer(text)
    await message.answer_document(ss)


class AddImage(StatesGroup):
    image = State()


# Еужно было некоторые фоточки в бд хранить


@my_router.message(F.text == 'Добавить фото')
async def get_add_image(message: Message, state: FSMContext):
    await message.answer("Отправьте фото")
    await state.set_state(AddImage.image)


@my_router.message(AddImage.image, F.photo)
async def add_iamge(message: Message, state: FSMContext, session: AsyncSession):
    image_id = message.photo[-1].file_id
    caption = message.caption.strip()
    if not caption:
        caption = 'Без описания'
    await orm_add(session=session, tablename='LikeImage', data={'image': image_id, 'caption': caption})
    await message.answer("Фото добалено")
    await state.clear()


# ловим некоррекный ввод
@my_router.message(AddImage.image)
async def add_image2(message: Message, state: FSMContext):
    if message.text.lower() == 'отмена':
        await message.answer('Действие отменено')
        await state.clear()
    else:
        await message.answer("Отправьте фото")


@my_router.message(F.text == 'Просмотр фото')
async def get_image(message: Message, session: AsyncSession):
    photos = await orm_get(session=session, tablename='LikeImage')
    media = []
    for photo in photos:
        media.append(InputMediaPhoto(media=photo.image, caption=photo.caption))
    await message.answer_media_group(media=media)
