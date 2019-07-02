# Purpose

This is the source code for the 3cosystem.com project. It contains the code for the website and the firehose.


## The Webapp

This is a standard django app,

# Requirements

  - Python 3.6
  - Postgresql with postgis (We use some of the distance functions)
  - Docker is helpful but not required

# Development
Standing up a local development environment is simple

  1. Create your database with `create database "3cosystem"` or another database tool
  1. Copy `env.sample` to `env`.
  1. Update the values in the `env` to match the credentials for your database, sentry, and email server
  1. setup your virtual environment. I use PyCharm, but you can use `python -m venv venv`
  1. install requirements with `pip install -r requirements.txt`
  1. migrate the database: `./manage.py migrate`
  1. import some fixtures: `./manage.py loaddata data/geography`
  1. create your superuser: `./manage.py createsuperuser`
  1. create your cache table: `./manage.py createcachetable`
  1. start the firehose task in a separate terminal: `./manage.py firehose`
  1. start your web process: `./manage.py runserver 0.0.0.0:8000` 
  
You are now ready to start development.   

## Task runners
There is a `Makefile` task-runner to help you run database migrations and load fixtures.  

Just type `make` in the root folder to see which commands are available

# The architecture is simple

There are two parts; the Firehose and the web process.
 
## The Firehose
This is a Django command that runs as a daemon. It connects to the Meetup.com API and consumes the feed of events fired 
from there. Any tech events are then parsed and inserted into the database

## The web process
This is just a plain vanilla django web app. It connects to the same database as the firehose and displays the events
to web users. 


