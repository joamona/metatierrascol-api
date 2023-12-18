# Bien venido al proyecto Metatierras Colombia

Metatierras colombia es un proyecto financiado por la Universitat Politècnica de València, 
y realizado en colaboración con la fundación Forjado Futuros.

El objetivo del proyecto es diseñar software libre para la agilización de la regularización 
de tierras rústicas en Colombia.

Este repositorio contiene parte de la implementación del diseño. Contiene un proyecto Django 
con la API REST, realizada con Django Rest Framework, que permite la interacción con la
base de datos.

# Instalación
1. Instalar Docker y Docker Compose
2. Clonar el repositorio
	
	https://github.com/joamona/metatierrascol-api.git

3. Ejecutar:

	docker-compose up

En la carpeta donde está el fichero .yml
La primera vez al inicializar con docker-compose up, se crean las imágenes y los contenedores,
pero servicio db tarda mucho porque debe crear el volumen de datos y no se inicia bien la API.

Detener los contenedores:

	control + c

o 

	doker-compose stop

Arrancar los contenedores de nuevo:
docker-compose up

Para inicializar la base de datos hay que ejecutar un script localizado en un contenedor:
**Nota: Puede que el nombre del volumen y del contenedor (metatierrascol-api_metatierrascol-data, metatierrascol-api_metatierrascol_1 sea diferente en su ordenador).**

	docker exec -it metatierrascol-api_metatierrascol_1 sh -c "./initdb.sh"

Esto solo hay que hacerlo la primera vez que se instalan los contenedores.

4. Visite la página de administración

	http://localhost:8000/admin

Usuario: admin, contraseña admin

Puede ver detalles de la api en:

	http://localhost:8000/swagger/
	http://localhost:8000/redoc/

Para reiniciar la base de datos, hay que borrar el volumen:

	docker-compose down
 	docker volume rm metatierrascol-api_metatierrascol-data

y volver al primer paso de la instalación.


