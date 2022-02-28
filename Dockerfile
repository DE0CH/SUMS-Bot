FROM python:3.8-alpine
WORKDIR /usr/app
RUN apk update && apk add python3-dev \
                        gcc \
                        libc-dev
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
CMD jurigged bot.py
