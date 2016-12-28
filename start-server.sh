python /app/manage.py collectstatic --noinput

# depending on the environment, (dev is default)
case "$DEV_ENV" in

    prod)
        # logs are output to stdout so other logging tools can pick them up
        /usr/local/bin/gunicorn config.wsgi -w 4 -b 0.0.0.0:5000 --chdir=/app
        ;;

    test)
        /usr/local/bin/gunicorn config.wsgi -w 4 -b 0.0.0.0:5000 --chdir=/app
        ;;
    *)
        # output logs to /logs folder
        python /app/manage.py migrate
        python /app/manage.py runserver 0.0.0.0:8000

esac
