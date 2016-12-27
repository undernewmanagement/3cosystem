FROM python:2-onbuild

# Requirements have to be pulled and installed here, otherwise caching won't work
COPY ./src/requirements.txt /requirements.txt

RUN pip install -r /requirements.txt \
    && groupadd -r django \
    && useradd -r -g django django

COPY src/ /app
RUN chown -R django /app


COPY ./start-server.sh /start-server.sh
COPY ./entrypoint.sh /entrypoint.sh

WORKDIR /app

ENTRYPOINT ["/entrypoint.sh"]
