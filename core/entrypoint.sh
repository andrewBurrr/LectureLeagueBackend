#!/bin/sh

python manage.py collectstatic --no-input
python manage.py flush --no-input
python manage.py makemigrations
python manage.py migrate

python manage.py loaddata users.json
python manage.py loaddata institutions.json
python manage.py loaddata courses.json

exec "$@"
