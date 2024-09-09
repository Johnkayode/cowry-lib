#!/bin/bash

python manage.py migrate --no-input

TESTING=1 python manage.py test api/apps

python manage.py runserver 0.0.0.0:8000