#/bin/sh

python manage.py shell < scripts/001_create_tables.py
python manage.py shell < scripts/002_init_snr_persona_titular_tipo.py
python manage.py shell < scripts/003_init_municipalities.py







python manage.py makemigrations
python manage.py migrate
DJANGO_SUPERUSER_PASSWORD=${DJANGO_SUPERUSER_PASSWORD} python manage.py createsuperuser --noinput --username ${DJANGO_SUPERUSER_USERNAME} --email ${DJANGO_SUPERUSER_EMAIL}