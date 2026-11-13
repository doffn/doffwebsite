#!/bin/bash
set -e
pip install -r requirements.txt

python manage.py runserver
python manage.py collectstatic --noinput
