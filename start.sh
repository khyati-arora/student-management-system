#!/bin/sh

# Run migrations
python manage.py migrate --noinput

# Create superuser if the environment variable is set
if [ "$CREATE_SUPERUSER" = "true" ]; then
  python manage.py createsuperuser --noinput --username $DJANGO_SUPERUSER_USERNAME --email $DJANGO_SUPERUSER_EMAIL 
fi

# Start the Django server
exec "$@"