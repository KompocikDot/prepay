ARG NODE_VERSION=18.16.0

FROM node:${NODE_VERSION}-alpine AS node

FROM python:3.11.8-alpine


# Installing node to the python container
COPY --from=node /usr/lib /usr/lib
COPY --from=node /usr/local/lib /usr/local/lib
COPY --from=node /usr/local/include /usr/local/include
COPY --from=node /usr/local/bin /usr/local/bin

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN apk --no-cache add \
	icu-dev \
	gettext \
	gettext-dev


RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .
