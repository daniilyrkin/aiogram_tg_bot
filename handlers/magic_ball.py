import random
from aiogram import Router
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from state_handlers import state as st

import os
from dotenv import load_dotenv
from keyboards.keyboards import Keyboards_all as key

magic_ball_routers = Router()
load_dotenv()

ADMIN = int(os.getenv('ADMIN'))

answers = [
    'Бесспорно', 'Мне кажется - да', 'Пока неясно, попробуй снова', 'Даже не думай',
    'Предрешено', 'Вероятнее всего', 'Спроси позже', 'Мой ответ - нет',
    'Никаких сомнений', 'Хорошие перспективы', 'Лучше не рассказывать', 'По моим данным - нет',
    'Определённо да', 'Знаки говорят - да', 'Сейчас нельзя предсказать', 'Перспективы не очень хорошие',
    'Можешь быть уверен в этом', 'Да', 'Сконцентрируйся и спроси опять', 'Весьма сомнительно']


@magic_ball_routers.message(Command('magic_ball'))
async def magic_ball_question(message: Message, state: FSMContext):
    key = ReplyKeyboardBuilder()
    key.button(text='Выход')
    await message.answer(
        'Задай вопрос или нажми кнопку для выхода',
        reply_markup=key.as_markup(
            resize_keyboard=True,
            input_field_placeholder="Нажми кнопку для выхода"))
    await state.set_state(st.Question_ball.question)


@magic_ball_routers.message(st.Question_ball.question)
async def magic_ball_answer(message: Message, state: FSMContext):
    user_msg = message.text
    if user_msg == 'Выход':
        await state.clear()
        await message.answer('Возвращайся если возникнут вопросы!', reply_markup=await key.start_key())
    else:
        answe = random.choice(answers)
        await message.answer(f'Ваш вопрос: {user_msg}\nМой ответ: {answe}'
                             '\nЗадай еще вопрос или нажми кнопку для выхода')
