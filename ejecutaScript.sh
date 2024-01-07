#/bin/bash

docker exec -it metatierrascol-api_metatierrascol_1 sh -c "python manage.py shell < script/011_init_usuarios_avisados_descarga_zip.py"
