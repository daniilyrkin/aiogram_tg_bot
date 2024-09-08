import requests
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.filters import CommandObject

import os
from dotenv import load_dotenv

books_router = Router()
load_dotenv()

ADMIN = int(os.getenv('ADMIN'))
books_router.message.filter(F.chat.id.in_({ADMIN}))


@books_router.message(Command(commands=['books']))
async def books_get(message: Message, command: CommandObject):
    command_args: str = command.args
    point = 'https://www.googleapis.com/books/v1/volumes'

    params = {'q': command_args, 'maxResults': 5}
    response = requests.get(point, params=params).json()

    text_books = ''

    for book in response['items']:
        volume = book['volumeInfo']
        title = volume['title']
        published = volume.get('publishedDate', 'год издания неизвестен')
        desription = volume.get('description', 'описание отсутсвует')
        text_books += f'{title} ({published}) \n {desription}\n''------------------------------\n'

    text = str(text_books)
    print(text)
    await message.answer(text=text)
