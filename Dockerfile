FROM python:3.9-buster
ENV BOT_NAME=$BOT_NAME

WORKDIR /usr/src/app/"${BOT_NAME:-tg_bot}"

COPY requirements.txt /usr/src/app/"${BOT_NAME:-tg_bot}"
RUN apt-get update && apt-get -y install postgresql-11
RUN pip install -r /usr/src/app/"${BOT_NAME:-tg_bot}"/requirements.txt
COPY . /usr/src/app/"${BOT_NAME:-tg_bot}"
