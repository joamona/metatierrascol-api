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
print('CREATE SCHEMA IF NOT EXISTS baunit')
oc.cursor.execute('create schema baunit')

print('CREATE SCHEMA IF NOT EXISTS codelist')
oc.cursor.execute('create schema codelist')

print('CREATE SCHEMA IF NOT EXISTS core')
oc.cursor.execute('create schema core')

print('CREATE SCHEMA IF NOT EXISTS party')
oc.cursor.execute('create schema party')

print('CREATE SCHEMA IF NOT EXISTS rrr')
oc.cursor.execute('create schema rrr')

print('CREATE SCHEMA IF NOT EXISTS source')
oc.cursor.execute('create schema source')

print('CREATE SCHEMA IF NOT EXISTS spatialunit')
oc.cursor.execute('create schema spatialunit')

#creación de tablas
#APP CODELIST
print('create table codelist.departamento')
oc.cursor.execute('CREATE TABLE IF NOT EXISTS codelist.departamento (id serial primary key, departamento varchar, unique(departamento))')

print('create table codelist.provincia')
oc.cursor.execute('CREATE TABLE IF NOT EXISTS codelist.provincia (id serial primary key, provincia varchar, unique(provincia))')

print('create table codelist.municipio ')
oc.cursor.execute('CREATE TABLE IF NOT EXISTS codelist.municipio (id serial primary key, departamento varchar, provincia varchar, codigo_municipio integer unique, nombre_municipio varchar, unique (codigo_municipio, nombre_municipio))')

print('create table codelist.snr_persona_titular_tipo')
oc.cursor.execute('CREATE TABLE IF NOT EXISTS codelist.snr_persona_titular_tipo (id serial primary key, snr_persona_titular_tipo varchar, unique (snr_persona_titular_tipo))')

print('create table codelist.sector')
oc.cursor.execute('CREATE TABLE IF NOT EXISTS codelist.sector (id serial primary key, sector varchar, unique (sector))')

print('create table codelist.lc_prediotipo')
oc.cursor.execute('CREATE TABLE IF NOT EXISTS codelist.lc_prediotipo (id serial primary key, lc_prediotipo varchar, unique (lc_prediotipo))')

print('create table codelist.estado_expediente')
oc.cursor.execute('CREATE TABLE IF NOT EXISTS codelist.estado_expediente (id serial primary key, estado_expediente varchar, unique (estado_expediente))')

#APP CORE
print('create table core.appsettings')
oc.cursor.execute('CREATE TABLE IF NOT EXISTS core.appsettings (id serial primary key, parameter_name varchar unique, parameter_value varchar, help_en varchar, help_es varchar)')

#almacena los usuarios y los municipios a los que tiene acceso
print('create table core.acceso_municipio')
oc.cursor.execute('CREATE TABLE IF NOT EXISTS core.acceso_municipio (id serial primary key, user_id integer not null, municipio_id integer not null, unique(user_id, municipio_id))')

#almacena los usuarios que reciben un email cuando se recibe un fichero
print('create table core.usuarios_avisados_descarga_zip')
oc.cursor.execute('CREATE TABLE IF NOT EXISTS core.usuarios_avisados_descarga_zip (id serial primary key, user_id integer not null, unique(user_id))')

#APP BAUNIT
print('create table baunit.baunit')
oc.cursor.execute("""CREATE TABLE IF NOT EXISTS baunit.baunit
                  (
                    id serial primary key,
                    numero_predial varchar,
                    nombre varchar,
                    tipo_id integer not null,
                    complemento varchar,
                    departamento_id integer not null,
                    provincia_id integer not null,
                    sector_predio_id integer not null,
                    municipio_id integer not null,
                    creado_por_id integer not null,
                    fecha_creacion timestamp not null,
                    codigo_acceso varchar not null,
                    estado_expediente_id integer not null,
                    longitud float,
                    latitud float,
                    numero_catastral varchar
                  )"""
)

#APP SOURCE
print('create table source.fichero_zip')
oc.cursor.execute("""CREATE TABLE IF NOT EXISTS source.archivo_zip
                  (
                    id serial primary key,
                    baunit_id integer not null,
                    creado_por_id integer not null,
                    fecha_creacion timestamp not null,
                    descargado_por_id integer,
                    fecha_descarga timestamp,
                    archivo varchar,
                    url_descarga varchar,
                    unique(baunit_id)
                  )"""
)

#integridad referencial
#BAUNIT
oc.cursor.execute('ALTER TABLE baunit.baunit ADD CONSTRAINT fk_baunit_departamento FOREIGN KEY (departamento_id) REFERENCES codelist.departamento(id) on delete no action on update cascade')
oc.cursor.execute('ALTER TABLE baunit.baunit ADD CONSTRAINT fk_baunit_proincia FOREIGN KEY (provincia_id) REFERENCES codelist.provincia(id) on delete no action on update cascade')
oc.cursor.execute('ALTER TABLE baunit.baunit ADD CONSTRAINT fk_baunit_sector_predio FOREIGN KEY (sector_predio_id) REFERENCES codelist.sector(id) on delete no action on update cascade')
oc.cursor.execute('ALTER TABLE baunit.baunit ADD CONSTRAINT fk_baunit_municipio FOREIGN KEY (municipio_id) REFERENCES codelist.municipio(id) on delete no action on update cascade')
oc.cursor.execute('ALTER TABLE baunit.baunit ADD CONSTRAINT fk_baunit_tipo FOREIGN KEY (tipo_id) REFERENCES codelist.Lc_prediotipo(id) on delete no action on update cascade')
oc.cursor.execute('ALTER TABLE baunit.baunit ADD CONSTRAINT fk_baunit_creado_por FOREIGN KEY (creado_por_id) REFERENCES auth_user(id) on delete no action on update cascade')
oc.cursor.execute('ALTER TABLE baunit.baunit ADD CONSTRAINT fk_baunit_estado_expediente FOREIGN KEY (estado_expediente_id) REFERENCES codelist.estado_expediente(id) on delete no action on update cascade')

#CORE
oc.cursor.execute('ALTER TABLE core.acceso_municipio ADD CONSTRAINT fk_acceso_municipio_username FOREIGN KEY (user_id) REFERENCES auth_user(id) on delete no action on update cascade')
oc.cursor.execute('ALTER TABLE core.acceso_municipio ADD CONSTRAINT fk_acceso_municipio_municipio FOREIGN KEY (municipio_id) REFERENCES codelist.municipio(id) on delete no action on update cascade')
oc.cursor.execute('ALTER TABLE core.usuarios_avisados_descarga_zip ADD CONSTRAINT fk_usuarios_avisados_descarga_zip_username FOREIGN KEY (user_id) REFERENCES auth_user(id) on delete no action on update cascade')

#SOURCE
oc.cursor.execute('ALTER TABLE source.archivo_zip ADD CONSTRAINT fk_source_archivo_zip_baunit FOREIGN KEY (baunit_id) REFERENCES baunit.baunit(id) on delete no action on update cascade')
oc.cursor.execute('ALTER TABLE source.archivo_zip ADD CONSTRAINT fk_source_archivo_zip_creado_por FOREIGN KEY (creado_por_id) REFERENCES auth_user(id) on delete no action on update cascade')
oc.cursor.execute('ALTER TABLE source.archivo_zip ADD CONSTRAINT fk_source_archivo_zip_descargado_por FOREIGN KEY (descargado_por_id) REFERENCES auth_user(id) on delete no action on update cascade')




oc.commit()
