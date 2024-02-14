# Bienvenido al proyecto Metatierras Colombia

Metatierras Colombia es un proyecto ADSIDEO financiado por el área de cooperación al desarrollo de la <a href='https://www.upv.es/'>Universitat Politècnica de València</a>, 
y realizado en colaboración con la <a href='https://www.forjandofuturos.org/'> Fundación Forjado Futuros</a>, y con la <a href="https://www.acpp.com/">Asamblea de Cooperación por la Paz</a>.

El objetivo del proyecto es diseñar software libre para la agilización de la regularización 
de tierras rústicas en Colombia.

Este repositorio contiene parte de la implementación del diseño. Contiene un proyecto Django 
con la API REST, realizada con Django Rest Framework, que permite la interacción con la
base de datos.

Esta API recibe los datos de la aplicación móvil de toma de datos de campo, y permite luego la descarga a usuarios autorizados, mediante un geoportal. Tanto la app, como el geoportal están todavía en desarrollo. Estamos dando los primeros pasos.

# Instalación

1. Instalar Docker y Docker Compose

2. Clonar el repositorio
	
	git clone https://github.com/joamona/metatierrascol-api.git

3. Arrancar los contenedores:

En la carpeta donde está el fichero .yml, ejecutar:

	docker-compose up -d

4. Inicializar la base de datos

Es necesario crear una base de datos con tablas y datos iniciales para que la API funcione. Para inicializar la base de datos hay que ejecutar un script localizado en un contenedor:

**Nota: En lo siguiente aparecen nombres de contenedores. Puede que el nombre del volumen, y del contenedor, refererido (metatierrascol-api_metatierrascol-data, metatierrascol-api_metatierrascol_1) sea diferente en su ordenador. Puede ver los nombres asignados en su ordenador con los comandos docker ps y docker volume ls**

	docker exec -it metatierrascol-api_metatierrascol_1 sh -c "./initdb.sh"

Solo es necesario inicializar la base de datos una vez. La primera vez que se instalan los contenedores.

5. Visitar la página de administración

Usuario: admin, contraseña admin

	http://localhost:8000/admin

Puede ver detalles de la api en:

	http://localhost:8000/swagger/
	http://localhost:8000/redoc/

6. Reiniciar la base de datos

Para el desarrollo, puede que necesite reiniciar la base de datos, para añadir nuevas tablas, o borrar datos de pruebas. Realice los siguientes pasos:

- Detenga y borre los contenedores:

	docker-compose down

- Elimine el volumen que contiene los datos de la base de datos.

 	docker volume rm metatierrascol-api_metatierrascol-data

- Vuelva al paso 3 de la instalación.


