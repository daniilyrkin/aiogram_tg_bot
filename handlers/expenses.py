from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

import os
import datetime
from dotenv import load_dotenv
from database.orm_query import orm_add, orm_get

from config import bot
from state_handlers import state as st

expenses_router = Router()
load_dotenv()

ADMIN = int(os.getenv('ADMIN'))
expenses_router.message.filter(F.chat.id.in_({ADMIN}))


@expenses_router.message(Command('траты'))
async def expenses(message: Message):
    key = InlineKeyboardBuilder()
    key.button(text='добавить расходы', callback_data='add_expenses')
    key.button(text='расходы месяц', callback_data='expenses_m')
    key.button(text='все рассходы', callback_data='all_expenses')
    key.adjust(1)
    await message.answer(
        text='Выберите',
        reply_markup=key.as_markup(
            resize_keyboard=True,
            input_field_placeholder="Нажми уже что-нибудь..."))


@expenses_router.callback_query(F.data == 'add_expenses')
async def add_expenses_0(callback: CallbackQuery, state: FSMContext):
    await bot.send_message(
        chat_id=callback.from_user.id,
        text='Какая сумма потрачена?')
    await state.set_state(st.Expenses.money)


@expenses_router.message(st.Expenses.money)
async def add_expenses_1(message: Message, state: FSMContext):
    key = ReplyKeyboardBuilder()
    key.button(text='Продукты')
    key.button(text='Ежемесячно')
    key.button(text='Прочее')
    key.adjust(2)
    await message.answer(
        text='На что потрачено?',
        reply_markup=key.as_markup(resize_keyboard=True))
    await state.update_data(amount=message.text)
    await state.set_state(st.Expenses.expenses_name)


@expenses_router.message(st.Expenses.expenses_name)
async def add_expenses_2(message: Message, state: FSMContext, session: AsyncSession):
    user_msg = message.text
    await state.update_data(expenses_name=user_msg)
    await orm_add(session=session, tablename='Expenses', data=await state.get_data())
    await state.clear()
    await message.answer(text='Получилось')


@expenses_router.callback_query(F.data.in_({'all_expenses', 'expenses_m'}))
async def all_expenses(callback: CallbackQuery, session: AsyncSession):
    await callback.answer()
    data = callback.data
    get_expenses = await orm_get(session=session, tablename='Expenses')
    date_now = datetime.date.today()
    text = 'Список расходов\n''-----------------------------'
    all_money = 0
    for expenses in get_expenses:
        print(data)
        date = datetime.datetime.strptime(str(expenses.created), '%Y-%m-%d %H:%M:%S')
        money = expenses.amount
        expenses_name = expenses.expenses_name
        if data == 'expenses_m':
            if date.date() == date_now:
                text += (
                    f'\n{expenses.created} \nПокупка: {expenses_name} \nНа сумму: {money}₽'
                    '\n-----------------------------')
                all_money += money
        else:
            text += (
                f'\n{date} \nПокупка: {expenses_name} \nНа сумму: {money}₽'
                '\n-----------------------------')
            all_money += money
    await callback.message.answer(text=f'{text}\n{all_money}₽')
