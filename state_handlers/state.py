from aiogram.fsm.state import State, StatesGroup


class InvestState(StatesGroup):
    Money_Up = State()


class Expenses(StatesGroup):
    money = State()
    expenses_name = State()


class Question_ball(StatesGroup):
    question = State()


class Add_product(StatesGroup):
    name = State()


class Music_yt(StatesGroup):
    links = State()
