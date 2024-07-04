'''
Created on Dec 6, 2023

@author: joamona
'''
from core.commonlibs import managePermissions

print("Creando grupos")
managePermissions.addOrGetGroup('admin')
managePermissions.addOrGetGroup('propietario')
managePermissions.addOrGetGroup('agrimensor')
managePermissions.addOrGetGroup('ant')
managePermissions.addOrGetGroup('gestor_catastral')
managePermissions.addOrGetGroup('snr')
managePermissions.addOrGetGroup('igac')
print("Grupos creados: admin,propietario,agrimensor,ant,gestor_catastral,snr,igac")
