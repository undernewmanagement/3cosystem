#!/usr/bin/env bash

/app/manage.py collectstatic --noinput
/app/manage.py migrate
/app/manage.py createcachetable
