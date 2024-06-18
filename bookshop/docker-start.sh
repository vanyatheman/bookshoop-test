#!/usr/bin/env bash

set -ex

python manage.py migrate

python manage.py collectstatic --noinput

# gunicorn bookshop.wsgi:application \
#   --bind 0.0.0.0:8000 \
#   "--reload" \
#   --chdir /app \
#   --access-logfile '-' \
#   --error-logfile '-' \
#   --capture-output
python manage.py runserver 0.0.0.0:8000
