#/bin/sh
#python remove_migration_files.py  -->No necesario git ya no sigue los ficheros de las migraciones
python manage.py makemigrations
python manage.py migrate
DJANGO_SUPERUSER_PASSWORD=${DJANGO_SUPERUSER_PASSWORD} python manage.py createsuperuser --noinput --username ${DJANGO_SUPERUSER_USERNAME} --email ${DJANGO_SUPERUSER_EMAIL}

python manage.py shell < script/001_create_schemas_and_tables.py
python manage.py shell < script/003_create_groups.py
python manage.py shell < script/004_create_users.py
python manage.py shell < script/005_init_lc_prediotipo.py
python manage.py shell < script/006_init_municipalities.py
python manage.py shell < script/007_init_snr_persona_titular_tipo.py
python manage.py shell < script/008_init_sector.py
python manage.py shell < script/009_init_estado_expediente_predio.py
python manage.py shell < script/010_init_appsettings.py
python manage.py shell < script/011_init_usuarios_avisados_descarga_zip.py
python manage.py shell < script/012_create_tables_mobileappversion.py








