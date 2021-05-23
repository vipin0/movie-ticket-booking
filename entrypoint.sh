#!/bin/sh
# export PATH="$HOME/.local/bin:$PATH"
sh -c "python manage.py makemigrations && python manage.py migrate && python manage.py collectstatic --noinput && gunicorn movie_booking.wsgi:application --bind :8000 --workers 3"