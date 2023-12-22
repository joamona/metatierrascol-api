#/bin/sh
python manage.py shell < script/001_create_tables.py

python manage.py migrate
DJANGO_SUPERUSER_PASSWORD=${DJANGO_SUPERUSER_PASSWORD} python manage.py createsuperuser --noinput --username ${DJANGO_SUPERUSER_USERNAME} --email ${DJANGO_SUPERUSER_EMAIL}

python manage.py makemigrations
python manage.py migrate







