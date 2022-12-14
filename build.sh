#!/usr/bin/env bash
# exit on error
set -o errexit

pip install --upgrade pip

pip install -r requirements_prod.txt

python manage.py collectstatic --no-input
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata mydata.json
python manage.py test
