import os
from os import listdir
from os.path import isfile, join

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def  list_files_in_folder(folder):
    """
    Returns the entire name of the files of a folder
    @type folder: string 
    @param folder: '/var/www/apps/desweb/dw_pozossan_sessions/templates'
    @return: ['/var/www/apps/desweb/dw_pozossan_sessions/templates/aa3.txt', '/var/www/apps/desweb/dw_pozossan_sessions/templates/mount_page.py', '/var/www/apps/desweb/dw_pozossan_sessions/templates/__init__.py', '/var/www/apps/desweb/dw_pozossan_sessions/templates/aa.txt', '/var/www/apps/desweb/dw_pozossan_sessions/templates/aa2.txt']
    """
    mi_path = folder
    list_files = []
    for f in listdir(mi_path):
        name_file=join(mi_path, f)
        if isfile(name_file):
            list_files.append(name_file)
    return list_files

def borrar_ficheros_excepto_init(carpetas):
    """
    Borra una carpeta
    """
    for carpeta in carpetas: 
        print(f'Borrando ficheros de la carpeta {carpeta}')
        carpeta=BASE_DIR + '/' + carpeta
        lf=list_files_in_folder(carpeta)
        for f in lf:
            if os.path.isfile(f):
                if '__init__.py' not in f:
                    print(f"Borrando fichero {f}")
                    os.remove(f)
            else:
                print(f'El fichero {f} no existe')
    return True

migration_folders=[
    'baunit/migrations',
    'codelist/migrations',
    'core/migrations',
    'party/migrations',
    'rrr/migrations',
    'source/migrations',
    'spatialunit/migrations',
    'mobileappversion/migrations'
]

borrar_ficheros_excepto_init(migration_folders)