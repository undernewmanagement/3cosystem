FROM python:3

# Pass the command line arg into the ENV arg, persisting it in the docker image
ARG SITE_VERSION
ENV SITE_VERSION=$SITE_VERSION

# Install binutils so that geodjango works
RUN apt-get update \
    && apt-get install -y binutils libproj-dev gdal-bin

# Requirements have to be pulled and installed here, otherwise caching won't work
COPY ./src/requirements.txt /requirements.txt

RUN pip install -r /requirements.txt \
    && groupadd -r django \
    && useradd -r -g django django \
    && mkdir /app 

COPY src /app
RUN chown -R django /app

COPY start-server.sh /start-server.sh
COPY entrypoint.sh /entrypoint.sh
COPY Procfile /app
RUN chmod +x /*.sh

EXPOSE 5000

ENTRYPOINT ["/entrypoint.sh"]
CMD ["/start-server.sh"]
