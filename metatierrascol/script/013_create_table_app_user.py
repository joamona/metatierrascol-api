'''
Created on Dec 6, 2023

@author: joamona
'''
import os
from django.db import connection
from pgOperations.pgOperations import PgConnection, FieldsAndValues
from core.commonlibs import generalModule, tokens
from django.contrib.auth.models import User

oc=PgConnection(connection)

print('create table core.app_user')
oc.cursor.execute('CREATE TABLE IF NOT EXISTS core.app_user (id serial primary key, user_id integer unique not null, data_acceptation boolean not null, notification_acceptation boolean not null, interest varchar not null, email_confirm_token varchar, email_confirmed boolean default false)')
oc.cursor.execute('ALTER TABLE core.app_user ADD CONSTRAINT fk_app_user_username FOREIGN KEY (user_id) REFERENCES public.auth_user(id) on delete no action on update cascade')

DJANGO_SUPERUSER_EMAIL=os.getenv('DJANGO_SUPERUSER_EMAIL')
user = list(User.objects.filter(email=DJANGO_SUPERUSER_EMAIL))[0]
token=tokens.AccountActivationTokenGenerator().make_token(user)
d={'user_id':user.id,'data_acceptation':True,'notification_acceptation':True,
   'interest':'Administrar','email_confirm_token':token,'email_confirmed':True}
fieldsAndValues=FieldsAndValues(d)
pgo=generalModule.getDjangoPg()
print('Inserting super user into core.app_user')
pgo.pgInsert('core.app_user',fieldsAndValues)
oc.commit()
