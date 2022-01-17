FROM python:3.8-alpine
WORKDIR /usr/app
RUN apk update && apk add python3-dev \
                        gcc \
                        libc-dev
COPY . .
RUN pip install -r requirements.txt
CMD python bot.py
