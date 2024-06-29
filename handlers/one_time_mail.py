from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
import random
import string
import aiohttp
import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession
from database.orm_query import orm_get_one, orm_update

from utils.logger import logger
from keyboards.keyboards import Keyboards_all as keyboard


# Тут работал с апи одноразовой почты

load_dotenv()

ADMIN = int(os.getenv('ADMIN'))
mail_router = Router()
mail_router.message.filter(F.chat.id.in_({ADMIN}))

API = 'https://www.1secmail.com/api/v1/'
domain_list = [
    "1secmail.com",
    "1secmail.org",
    "1secmail.net",
    "wwjmp.com",
    "esiix.com",
    "xojxe.com",
    "yoggm.com"]


async def generate_username():
    domain = random.choice(domain_list)
    name = string.ascii_lowercase + string.digits
    username = ''.join(random.choice(name) for i in range(10))
    mail = f'{username}@{domain}'
    return mail


async def deleted_mail(session: AsyncSession, message, mail=''):
    url = 'https://www.1secmail.com/mailbox'
    data = {
        'action': 'deleteMailbox',
        'login': mail.split('@')[0],
        'domain': mail.split('@')[1]
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data) as response:
            print(response.status)
            await message.answer(f'[-] Почтовый адрес {mail} - удален!')
    mails = await orm_get_one(session=session, tablename='User', kwargs=f'id = {int(message.from_user.id)}')
    ssms = mails.one_time_mail.split(',')
    ssms.remove(mail)
    await orm_update(
        tablename='User',
        session=session,
        data={'one_time_mail': str(*ssms), 'username': message.from_user.username})


async def check_mail(message, mail=''):
    text_mail = ''
    req_mail = f'{API}?action=getMessages&login={mail.split("@")[0]}&domain={mail.split("@")[1]}'
    async with aiohttp.ClientSession() as session:
        async with session.get(req_mail) as response:
            data = await response.json()
        length = len(data)
        if length == 0:
            await message.answer('[-] Нет сообщений')
        else:
            id_list = []
            for i in data:
                for k, v in i.items():
                    if k == 'id':
                        id_list.append(v)
            await message.answer('[+] У вас есть сообщения')
            for i in id_list:
                read_msg = f'{API}?action=readMessage&login={mail.split("@")[0]}&domain={mail.split("@")[1]}&id={i}'
                async with session.get(read_msg) as response:
                    r = await response.json()
                    sender = r['from']
                    subject = r['subject']
                    date = r['date']
                    content = r['textBody']
                    text_mail += f'Отправитель: {sender}\nДата: {date}\nТема: {subject}\nСодержание: {content}'
            await message.answer(text_mail)


@mail_router.message(Command('get_mail_list'))
async def get_mail_list(message: Message):
    mails = await orm_get_one(tablename='User', kwargs=f'id = {int(message.from_user.id)}')
    if mails:
        await message.answer(f'Ваша(и) почта(ы): {str(mails.one_time_mail)}')
        ssms = mails.one_time_mail.split(',')
        for mail in ssms:
            keyboards = await keyboard.key_builder(list=ssms, args='delete_mail ')
            await message.answer(f'Проверка почты {mail}', reply_markup=keyboards)
            await check_mail(message, mail)
    else:
        await message.answer('У вас нет временной почты')


@mail_router.message(Command('one-time_mail'))
async def main(message: Message, session: AsyncSession):
    try:
        mail = await generate_username()
        mail_req = f'{API}?login={mail.split("@")[0]}&domain={mail.split("@")[1]}'
        async with aiohttp.ClientSession() as session_:
            async with session_.get(mail_req) as response:
                print(response.status)
                await message.answer(f'Ваша временная почта: {mail}')
        mail_user = await orm_get_one(tablename='User', kwargs=f'id = {int(message.from_user.id)}', session=session)
        if mail_user is not None:
            mails_user = f"{mail_user},{mail}"
            await orm_update(
                tablename='User',
                session=session,
                data={'one_time_mail': str(mails_user), 'username': message.from_user.username})
        else:
            await orm_update(
                tablename='User',
                session=session,
                data={'one_time_mail': str(mail_user), 'username': message.from_user.username})
        await logger(message=message, text=f'Создал почту {mail}')
    except Exception as ex:
        await logger(message=message, text=ex)


@mail_router.message(F.text.startswith('delete_mail'))
async def get_delete_mail(message: Message, session: AsyncSession):
    print(message.text)
    user_msg = message.text.split(' ')[1]
    await deleted_mail(mail=user_msg, message=message, session=session)
