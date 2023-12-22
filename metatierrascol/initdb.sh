#/bin/sh
python manage.py shell < script/002_init_snr_persona_titular_tipo.py
python manage.py shell < script/003_init_municipalities.py
python manage.py shell < script/004_init_sector.py
python manage.py shell < script/005_init_lc_prediotipo.py







