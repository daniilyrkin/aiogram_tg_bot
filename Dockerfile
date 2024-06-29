FROM python:3.11-slim

RUN apt-get install -yq tzdata
ENV TZ="Europe/Moscow"

RUN mkdir my_bot

WORKDIR /my_bot

ADD requirements.txt /my_bot/
RUN pip install -r requirements.txt
ADD . /my_bot/

ADD .docker.env /my_bot/.env

CMD python3.11 my_bot_tg.py

