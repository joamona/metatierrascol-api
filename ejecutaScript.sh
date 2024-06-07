#/bin/bash

docker exec -it metatierrascol-api-metatierrascol-1 sh -c "python manage.py shell < script/011_init_usuarios_avisados_descarga_zip.py"
