#!/bin/bash
python manage.py makemigrations
python manage.py makemigrations corsheaders
python manage.py makemigrations posts
python manage.py migrate
