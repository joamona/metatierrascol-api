from django.contrib.auth.models import User
from core.commonlibs import managePermissions

propietario=User(username='propietario@gmail.com', password='zzzxxxccc')
propietario.is_active=True
propietario.email=propietario.username
propietario.save()

agrimensor=User(username='agrimensor@gmail.com', password='zzzxxxccc')
agrimensor.is_active=True
agrimensor.email=agrimensor.username
agrimensor.save()

ant=User(username='ant@gmail.com', password='zzzxxxccc')
ant.is_active=True
ant.email=ant.username
ant.save()

gestor_catastral=User(username='gestor_catastral@gmail.com', password='zzzxxxccc')
gestor_catastral.is_active=True
gestor_catastral.email=gestor_catastral.username
gestor_catastral.save()

snr=User(username='snr@gmail.com', password='zzzxxxccc')
snr.is_active=True
snr.email=snr.username
snr.save()

igac=User(username='igac@gmail.com', password='zzzxxxccc')
igac.is_active=True
igac.email=igac.username
igac.save()

print('Usuarios de partida creados: admin, propietario, agrimensor, ant, snr, gestor_catastral e igac')

managePermissions.addUserToGroup(username='admin', groupname='admin')
managePermissions.addUserToGroup(username='propietario@gmail.com', groupname='propietario')
managePermissions.addUserToGroup(username='agrimensor@gmail.com', groupname='agrimensor')
managePermissions.addUserToGroup(username='ant@gmail.com', groupname='ant')
managePermissions.addUserToGroup(username='snr@gmail.com', groupname='snr')
managePermissions.addUserToGroup(username='igac@gmail.com', groupname='igac')

print('Usuarios añadidos a sus respectivos grupos')
