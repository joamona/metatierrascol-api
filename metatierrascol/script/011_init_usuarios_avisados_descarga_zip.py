'''
Created on Dec 6, 2023

@author: joamona

Añade la lista inicial de usuarios que reciben el email de aviso para la descarga
del fichero.

Creo las tablas manualmente porque Django, cuando las crea al hacer las migraciones,
no establece qué hacer ON UPDATE, en los campos de clave foránea.

Se establece ON DELETE NO ACTION. Esto evita que se puedan borrar filas de otras tablas,
si hay alguna referencia a la clave que se intenta borrar.
'''

from django.db import connection
from pgOperations.pgOperations import PgConnection, PgOperations, FieldsAndValues, WhereClause

l=['joamona@cgf.upv.es']

print('Inicializando usuarios avisados para la descarga')

oc=PgConnection(connection)
pgo=PgOperations(oc, global_print_queries=True)

for email in l:
    print(f'Usuario avisado: {email}')
    wh=WhereClause(where_clause='username=%s',where_values_list=[email])
    id_usuario = pgo.pgSelect(table_name='auth_user',string_fields_to_select='id',whereClause=wh)[0]['id']
    fa=FieldsAndValues({'user_id': id_usuario})
    pgo.pgInsert(table_name='core.usuarios_avisados_descarga_zip',fieldsAndValues=fa)

oc.commit()
