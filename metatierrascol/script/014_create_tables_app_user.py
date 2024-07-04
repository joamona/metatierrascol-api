'''
Created on Dec 6, 2023

@author: joamona
'''

from django.db import connection
from pgOperations.pgOperations import PgConnection
oc=PgConnection(connection)

#creación de tablas
print('create table core.app_user')
oc.cursor.execute('CREATE TABLE IF NOT EXISTS core.app_user (id serial primary key, user_id integer unique not null, data_acceptation boolean not null, notification_acceptation boolean not null, interest varchar not null, email_confirm_token varchar, email_confirmed boolean default false)')
oc.cursor.execute('ALTER TABLE core.app_user ADD CONSTRAINT fk_app_user_username FOREIGN KEY (user_id) REFERENCES public.auth_user(id) on delete no action on update cascade')

oc.commit()
