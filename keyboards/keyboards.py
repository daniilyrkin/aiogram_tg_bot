from aiogram.utils.keyboard import ReplyKeyboardBuilder


class Keyboards_all:

    async def expenses_key():
        key = ReplyKeyboardBuilder()
        key.button(text='Продукты')
        key.button(text='Ежемесячное')
        key.button(text='Прочее')
        return key.as_markup(
            resize_keyboard=True,
            input_field_placeholder="Выбери")

    async def start_key():
        keyboard = ReplyKeyboardBuilder()
        keyboard.button(text="/weather")
        keyboard.button(text="/user_id")
        keyboard.button(text='/download')
        keyboard.button(text='/magic_ball')
        return keyboard.as_markup(
            resize_keyboard=True,
            input_field_placeholder="Выбери")

    async def key_builder(list, args=None):
        keyboard = ReplyKeyboardBuilder()
        for item in list:
            if args is None:
                keyboard.button(text=item)
            else:
                keyboard.button(text=args + item)
        keyboard.adjust(2)
        return keyboard.as_markup(
            resize_keyboard=True)
