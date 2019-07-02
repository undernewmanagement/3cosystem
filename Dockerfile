FROM python:3.6-slim

# Pass the command line arg into the ENV arg, persisting it in the docker image
ARG SITE_VERSION
ENV SITE_VERSION=$SITE_VERSION
ENV PYTHONUNBUFFERED=1

# Install binutils so that geodjango works
RUN apt-get update \
    && apt-get install -y binutils libproj-dev gdal-bin

# Requirements have to be pulled and installed here, otherwise caching won't work
COPY requirements.txt /requirements.txt

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r /requirements.txt && \
    mkdir /app 

COPY src /app

WORKDIR /app

COPY env.sample /env.build
RUN ( set -a; . /env.build; set +a; python manage.py collectstatic --noinput)
RUN rm /env.build

CMD ["gunicorn", "wsgi:application", "-c", "gunicorn_config.py"]
