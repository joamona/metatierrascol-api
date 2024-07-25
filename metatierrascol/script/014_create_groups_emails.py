'''
Created on Dec 6, 2023

@author: joamona
'''
import os

from django.contrib.auth.models import Group
from core.commonlibs import managePermissions

print('Creando nuevos grupos para la gestión de usuarios')
Group.objects.get_or_create(name='receptor_email_nuevos_usuarios')
Group.objects.get_or_create(name='receptor_email_usuario_confirma_email')
Group.objects.get_or_create(name='receptor_email_usuario_sube_predio')
Group.objects.get_or_create(name='forjando_futuros')
print('Nuevos grupos creados')

DJANGO_SUPERUSER_EMAIL=os.getenv('DJANGO_SUPERUSER_EMAIL')
print(f'Añadiendo admin a los nuevos grupos: {DJANGO_SUPERUSER_EMAIL}')

managePermissions.addUserToGroup(username=DJANGO_SUPERUSER_EMAIL, groupname='receptor_email_nuevos_usuarios')
managePermissions.addUserToGroup(username=DJANGO_SUPERUSER_EMAIL, groupname='receptor_email_usuario_confirma_email')
managePermissions.addUserToGroup(username=DJANGO_SUPERUSER_EMAIL, groupname='receptor_email_usuario_sube_predio')
