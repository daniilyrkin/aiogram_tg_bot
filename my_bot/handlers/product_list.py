import random
from aiogram import Router, F
from aiogram.filters import Command, CommandObject
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from state_handlers import state as st

from keyboards.keyboards import Keyboards_all as key
from config import ADMIN

product_list_routers = Router()

product_list_routers.message.filter(F.chat.id.in_({ADMIN}))


# Хотел создать список покупок, потом стал переходить на алхимию. Не доделал вот...


@product_list_routers.message(Command('add'))
async def add_product(message: Message, state: FSMContext):
    await message.answer('Введи или выбери на что потрачено')
    key = ReplyKeyboardBuilder()
    key.add()
    await state.set_state(st.Add_product.name)


@product_list_routers.message(st.Add_product.name)
async def add_product_(message: Message, state: FSMContext):
    msg = message.text
    db.query('INSERT INTO product_list (product_name) VALUES (?)', (msg,))
    await message.answer(f'{msg}\nУспешно добавлено!')
    await state.clear()


@product_list_routers.message(Command('del'))
async def del_product(message: Message, command: CommandObject):
    command_args: str = command.args
    if command_args == 'all':
        db.query('DELETE FROM product_list')
        text = ('Список успешно очищен!')
    elif command_args:
        db.query('DELETE FROM product_list WHERE product_name = ?;', command_args)
        text = ('Успешно удалено')
    else:
        products = db.fetchall('SELECT * FROM product_list')
        if products:
            products_list = []
            for product in products:
                products_list.append(f'/del {product}')
            keyboard = key.key_builder(products_list)
        else:
            text = 'Список пуст'
    await message.answer(text=text, reply_markup=keyboard if keyboard else None)


@product_list_routers.message(Command('get'))
async def get_product(message: Message):
    products = db.fetchall('SELECT * FROM product_list')
    if products:
        text = ''
        for product, num in zip(products, random(len(products))):
            text += f'{num}. {product}'
    else:
        text = 'Список пуст'
    await message.answer(text)
