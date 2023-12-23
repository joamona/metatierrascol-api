#/bin/bash

docker exec -it metatierrascol-api_metatierrascol_1 sh -c "python manage.py shell < script/009_init_estado_expediente_predio.py"
