FROM python:3.8-slim

WORKDIR /usr/src/app

COPY ./pgsync ./

RUN chmod +x ./entrypoint.sh

RUN pip install pgsync

RUN apt update \
    && apt install -y moreutils \
    && apt install -y jq \
    && apt install -y wait-for-it

ENTRYPOINT ["bash", "./entrypoint.sh"]