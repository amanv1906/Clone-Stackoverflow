#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py migrate

echo "from django.contrib.auth.models import User;
User.objects.filter(username='admin', is_superuser=True).delete();
User.objects.create_superuser('admin', 'admin@gmail.com', 'admin1234')" | python manage.py shell

exec "$@"
