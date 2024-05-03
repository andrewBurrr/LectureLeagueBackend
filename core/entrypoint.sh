#!/bin/sh

python manage.py collectstatic --no-input
pthon manage.py flush --no-input
python manage.py migrate
python manage.py runserver

exec "$@"
