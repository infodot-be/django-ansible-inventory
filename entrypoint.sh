#!/bin/bash

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# python manage.py flush --no-input
python manage.py migrate
python manage.py makemigrations
python manage.py makemigrations api
python manage.py migrate
python manage.py collectstatic --no-input --clear

exec gunicorn inventory.wsgi:application --access-logfile - --error-logfile - --bind 0.0.0.0:8000 \
"$@"
