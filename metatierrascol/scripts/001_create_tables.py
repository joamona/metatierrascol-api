'''
Created on Dec 6, 2023

@author: joamona
'''

from django.db import connection
from pgOperations.pgOperations import PgConnection
oc=PgConnection(connection)

print('create schema codelist')
oc.cursor.execute('create schema codelist')

print('create table appsettings')
oc.cursor.execute('create table appsettings (gid serial primary key, parameter_name varchar unique, parameter_value varchar, help_en varchar, help_es varchar)')

print('create table codelist.municipio ')
oc.cursor.execute('create table codelist.municipio (gid serial primary key, departamento varchar, provincia varchar, codigo_municipio integer unique, nombre_municipio varchar, unique (codigo_municipio, nombre_municipio))')

oc.commit()

