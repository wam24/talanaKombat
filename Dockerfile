FROM python:3.10-alpine3.18

LABEL authors="wilhen"

RUN apk add --no-cache --virtual .build-deps \
                      curl
WORKDIR /app
COPY . .

RUN curl https://bootstrap.pypa.io/get-pip.py -o /get-pip.py  \
    && python /get-pip.py \
    && pip3 install --upgrade pip


RUN pip install -r requeriments.txt
