#!/bin/bash

# Build the project
echo "Building the project..."
python -m pip installl -r requirements.txt

echo "Make migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo "Collect Static..."
python manage.py collectstatic --noinput --clear