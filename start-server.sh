echo "Running start-server.sh..."

python /app/manage.py collectstatic --noinput

# depending on the environment, (dev is default)
case "$DEV_ENV" in

    prod)
        # logs are output to stdout so other logging tools can pick them up
        /usr/local/bin/gunicorn website.wsgi -w 4 -b 0.0.0.0:5000 --chdir=/app
        ;;

    test)
        /app/manage.py migrate
        /app/manage.py createcachetable
        /usr/local/bin/gunicorn website.wsgi -w 4 -b 0.0.0.0:5000 --chdir=/app
        ;;
    *)
        /app/manage.py migrate
        /app/manage.py createcachetable
        /app/manage.py runserver 0.0.0.0:5000

esac
