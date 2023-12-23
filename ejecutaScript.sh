#/bin/bash
docker exec -it metatierrascol-api_metatierrascol_1 sh -c "python manage.py shell < script/007_create_users.py"
