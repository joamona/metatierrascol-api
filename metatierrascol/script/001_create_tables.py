'''
Created on Dec 6, 2023

@author: joamona
'''

from django.db import connection
from pgOperations.pgOperations import PgConnection
oc=PgConnection(connection)

print('CREATE SCHEMA IF NOT EXISTS codelist')
oc.cursor.execute('create schema codelist')

#print('create table appsettings')
#oc.cursor.execute('CREATE TABLE IF NOT EXISTS appsettings (gid serial primary key, parameter_name varchar unique, parameter_value varchar, help_en varchar, help_es varchar)')

#print('create table codelist.departamento')
#oc.cursor.execute('CREATE TABLE IF NOT EXISTS codelist.departamento (gid serial primary key, departamento varchar, unique(departamento))')

#print('create table codelist.provincia')
#oc.cursor.execute('CREATE TABLE IF NOT EXISTS codelist.provincia (gid serial primary key, provincia varchar, unique(provincia))')

#print('create table codelist.municipio ')
#oc.cursor.execute('CREATE TABLE IF NOT EXISTS codelist.municipio (gid serial primary key, departamento varchar, provincia varchar, codigo_municipio integer unique, nombre_municipio varchar, unique (codigo_municipio, nombre_municipio))')

oc.commit()

