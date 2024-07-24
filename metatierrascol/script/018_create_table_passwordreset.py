'''
Created on Dec 6, 2023

@author: joamona

Creo las tablas manualmente porque Django, cuando las crea al hacer las migraciones,
no establece qué hacer ON UPDATE, en los campos de clave foránea.

Se establece ON DELETE NO ACTION. Esto evita que se puedan borrar filas de otras tablas,
si hay alguna referencia a la clave que se intenta borrar.
'''

from django.db import connection
from pgOperations.pgOperations import PgConnection
oc=PgConnection(connection)

print('create table core.custompasswordreset')
oc.cursor.execute('CREATE TABLE IF NOT EXISTS core.custompasswordreset (id serial primary key, email varchar unique not null, token varchar, created_at timestamp default now())')

oc.commit()
print('created')
