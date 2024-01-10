'''
Created on Dec 6, 2023

@author: joamona

Creo las tablas manualmente porque Django, cuando las crea al hacer las migraciones,
no establece qué hacer ON UPDATE, en los campos de clave foránea.

Se establece ON DELETE NO ACTION. Esto evita que se puedan borrar filas de otras tablas,
si hay alguna referencia a la clave que se intenta borrar.
'''

from django.db import connection
from pgOperations.pgOperations import PgConnection, PgOperations, FieldsAndValues

print('Inicializando app settings')

oc=PgConnection(connection)
pgo=PgOperations(oc, global_print_queries=True)

fa=FieldsAndValues({
    'parameter_name':'borrar_fichero_zip_al_descargar',
    'parameter_value': 'False',
    'help_en':'If True, deletes the .zip file with the field data on download de file at the first time',
    'help_es': 'Si es True, se borra el el fichero .zip con los datos de campo al descargarse por primera vez'})
pgo.pgInsert(table_name='core.appsettings',fieldsAndValues=fa)


fa=FieldsAndValues({
    'parameter_name':'tamaño_maximo_fichero_zip_mb',
    'parameter_value': '50',
    'help_en':'Maximum zip file size in megabytes',
    'help_es': 'Tamaño máximo dle fichero en megabytes'})
pgo.pgInsert(table_name='core.appsettings',fieldsAndValues=fa)



