#!/usr/bin/env bash

pip install -r requirements.txt

cd africonnect

python manage.py migrate

python manage.py collectstatic --noinput