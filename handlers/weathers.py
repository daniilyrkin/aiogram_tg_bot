from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from art import tprint
from datetime import datetime
import ujson
import requests
import time as tm
from dotenv import load_dotenv
import os

from config import bot
import logging

load_dotenv()

MS = int(os.getenv('ADMIN'))
apikey = os.getenv('APIKEY')
cities_id = os.getenv('cities_id')
name_of_cities = os.getenv('name_of_cities')

weather_router = Router()


@weather_router.message(Command('weather'))
async def user_weather(message: Message):
    await weather(message.from_user.id)


@weather_router.message(Command('update_weather'))
async def update_weather(message: Message):
    await message.answer('Updating...')
    await down_weather()


async def auto_weather():
    await weather_am(MS)


async def down_weather():
    tprint('Update to file...', font='tarty2')
    for city_id in cities_id:
        url = ('http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/'
               f'{city_id}?apikey={apikey}&language=ru'
               '&metric=True&details=True')
        req = requests.get(url)
        print(req)
        src = req.json()
        if int(datetime.now().strftime('%H')) >= 12:
            with open(f'handlers/weather/{city_id}_PM.json',
                      'w', encoding='UTF-8') as file:
                ujson.dump(src, file, indent=4, ensure_ascii=False)
            print(f"File {city_id}.json_PM updated.")
            logging.info(f"File {city_id}.json_PM updated.")
        else:
            with open(f'handlers/weather/{city_id}_AM.json',
                      'w', encoding='UTF-8') as file:
                ujson.dump(src, file, indent=4, ensure_ascii=False)
            print(f"File {city_id}_AM.json updated.")
            logging.info(f"File {city_id}.json_AM updated.")


async def weather_am(id):
    try:
        for (city_id, name_of_the_city) in zip(cities_id, name_of_cities):
            tm.sleep(0.5)
            with open(f'handlers/weather/{city_id}_AM.json',
                      'r', encoding='UTF-8') as file:
                for src in ujson.load(file):
                    time = src['DateTime']
                    time = int(time[11:13])
                    if time == 6:
                        print('the right time')
                        city = name_of_the_city
                        date = src['DateTime']
                        date = date[0:10]
                        temp = int(src["Temperature"]["Value"])
                        term = src['IconPhrase']
                        real_temp = int(src['RealFeelTemperatureShade']
                                        ['Value'])
                        Probability = src['PrecipitationProbability']
                        Rain = src['RainProbability']
                        Snow = src['SnowProbability']
                        Ice = src['IceProbability']
                        wind_speed = src['Wind']["Speed"]["Value"]
                        windgust = src["WindGust"]["Speed"]["Value"]
                    if time == 11:
                        temp_11 = int(src["Temperature"]["Value"])
                        term_11 = src['IconPhrase']
                        real_temp_11 = int(
                            src['RealFeelTemperatureShade']
                            ['Value'])
                        Probability_11 = src['PrecipitationProbability']
                        Rain_11 = src['RainProbability']
                        Snow_11 = src['SnowProbability']
                        Ice_11 = src['IceProbability']
                        wind_speed_11 = src['Wind']["Speed"]["Value"]
                        windgust_11 = src["WindGust"]["Speed"]["Value"]
                text = (
                    f'\n🌡<b>Температура:</b> {temp} ... {temp_11} ℃ '
                    f'\n☁ <b>На небушке:</b> {term} и {term_11} '
                    f'\n<b>По ощущению:</b> {real_temp} ... {real_temp_11} ℃.'
                    f'\n💨 <b>Скорость ветра:</b> {wind_speed} - '
                    f'{wind_speed_11} km/h'
                    f'\n💨 <b>С порывами до:</b> {windgust} - '
                    f'{windgust_11} km/h'
                    f'\n<b>Вероятность осадков:</b> {Probability} - '
                    f'{Probability_11}%'
                    f'\n 🌧 <b>Дождика:</b> {Rain} - {Rain_11}%'
                    f'\n 🌨 <b>Снежка:</b> {Snow}  - {Snow_11}%'
                    f'\n 🌨 <b>Градика:</b> {Ice} - {Ice_11}%'
                    f'\nДанные получены с сайта: AccuWeather.com'
                )
                await bot.send_message(
                    chat_id=id,
                    text=(
                        f'Погодка для {city} на {date} c 5 до 11 часов'
                        f'{text}'))
    except Exception as ex:
        msg = (f'Exception - {ex}')
        await bot.send_message(
            chat_id=MS,
            text=msg
        )


async def weather(id):
    for (city_id, name_of_the_city) in zip(cities_id, name_of_cities):
        tm.sleep(0.5)
        if int(datetime.now().strftime('%H')) >= 12:
            with open(f'handlers/weather/{city_id}_PM.json',
                      'r', encoding='UTF-8') as file:
                load_file = ujson.load(file)
        else:
            with open(f'handlers/weather/{city_id}_AM.json',
                      'r', encoding='UTF-8') as file:
                load_file = ujson.load(file)
        for src in load_file:
            time = src['DateTime']
            time = int(time[11:13])
            time_now = int(datetime.now().strftime('%H'))
            city = name_of_the_city
            date = src['DateTime']
            date = date[0:10]
            if time == time_now:
                print('the right time')
                temp = int(src["Temperature"]["Value"])
                term = src['IconPhrase']
                real_temp = int(src['RealFeelTemperatureShade']['Value'])
                Probability = src['PrecipitationProbability']
                Rain = src['RainProbability']
                Snow = src['SnowProbability']
                Ice = src['IceProbability']
                wind_speed = src['Wind']["Speed"]["Value"]
                windgust = src["WindGust"]["Speed"]["Value"]
            if time == (time_now + 1):
                temp_12 = int(src["Temperature"]["Value"])
                term_12 = src['IconPhrase']
                real_temp_12 = int(src['RealFeelTemperatureShade']
                                   ['Value'])
                Probability_12 = src['PrecipitationProbability']
                Rain_12 = src['RainProbability']
                Snow_12 = src['SnowProbability']
                Ice_12 = src['IceProbability']
                wind_speed_12 = src['Wind']["Speed"]["Value"]
                windgust_12 = src["WindGust"]["Speed"]["Value"]
        text = (
            f'\n🌡<b>Температура:</b> {temp} ... {temp_12} ℃ '
            f'\n☁ <b>На небушке:</b> {term} и {term_12} '
            f'\n<b>По ощущению:</b> {real_temp} ... {real_temp_12} ℃.'
            f'\n💨 <b>Скорость ветра:</b> {wind_speed} - {wind_speed_12} km/h'
            f'\n💨 <b>С порывами до:</b> {windgust} - {windgust_12} km/h'
            f'\n<b>Вероятность осадков:</b> {Probability} - {Probability_12}%'
            f'\n 🌧 <b>Дождика:</b> {Rain} - {Rain_12}%'
            f'\n 🌨 <b>Снежка:</b> {Snow}  - {Snow_12}%'
            f'\n 🌨 <b>Градика:</b> {Ice} - {Ice_12}%'
            f'\nДанные получены с сайта: AccuWeather.com'
        )
        await bot.send_message(
            chat_id=id,
            text=(
                f'Погодка для {city}'
                f'\nНа {date} в {time_now}:00 и {time_now + 1}:00'
                f'{text}'))
