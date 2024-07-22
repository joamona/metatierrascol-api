'''
Created on Dec 6, 2023

@author: joamona
'''
from django.contrib.auth.models import Group

from core.commonlibs import managePermissions

print('Creando nuevos grupos para la gestión de usuarios')
Group.objects.get_or_create(name='receptor_email_nuevos_usuarios')
Group.objects.get_or_create(name='receptor_email_usuario_confirma_email')
Group.objects.get_or_create(name='receptor_email_usuario_sube_predio')
Group.objects.get_or_create(name='forjando_futuros')
print('Nuevos grupos creados')

managePermissions.addUserToGroup(username='admin', groupname='receptor_email_nuevos_usuarios')
managePermissions.addUserToGroup(username='admin', groupname='receptor_email_usuario_confirma_email')
managePermissions.addUserToGroup(username='admin', groupname='receptor_email_usuario_sube_predio')
