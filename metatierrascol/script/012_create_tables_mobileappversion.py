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

#creación de esquemas
print('CREATE SCHEMA IF NOT EXISTS mobileappversion')
oc.cursor.execute('CREATE SCHEMA IF NOT EXISTS mobileappversion')

#creación de tablas
print('create table mobileappversion.mobileappversion')
oc.cursor.execute('CREATE TABLE IF NOT EXISTS mobileappversion.mobileappversion (id serial primary key, version double precision not null unique, archivo varchar not null unique, publicar boolean not null default false, fecha timestamp not null default now(), creado_por_id integer not null, url_descarga varchar)')
print('create table mobileappversion.mobileappversionnotes')
oc.cursor.execute('CREATE TABLE IF NOT EXISTS mobileappversion.mobileappversionnotes (id serial primary key, mobileappversion_id integer not null, fecha timestamp not null  default now(), nota varchar not null, creado_por_id integer not null)')

oc.cursor.execute('ALTER TABLE mobileappversion.mobileappversion ADD CONSTRAINT fk_mobileappversion_creado_por FOREIGN KEY (creado_por_id) REFERENCES auth_user(id) on delete no action on update cascade')
oc.cursor.execute('ALTER TABLE mobileappversion.mobileappversionnotes ADD CONSTRAINT fk_mobileappversionnotes_creado_por FOREIGN KEY (creado_por_id) REFERENCES auth_user(id) on delete no action on update cascade')
oc.cursor.execute('ALTER TABLE mobileappversion.mobileappversionnotes ADD CONSTRAINT fk_mobileappversion_id FOREIGN KEY (mobileappversion_id) REFERENCES mobileappversion.mobileappversion(id) on delete no action on update cascade')

oc.commit()
