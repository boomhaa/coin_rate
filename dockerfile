FROM python:latest

LABEL Maintainer="roushan.me17"

WORKDIR /usr/app/src


COPY main.py ./


CMD [ "python", "./test.py"]