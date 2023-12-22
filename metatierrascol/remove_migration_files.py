import shutil
import os, sys
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def borrar_carpetas(carpetas):
    """
    Borra una carpeta
    """
    for carpeta in carpetas:
        carpeta=BASE_DIR + '/' + carpeta
        if os.path.isdir(carpeta):
            print(f"Borrando carpeta {carpeta}")
            #shutil.rmtree(carpeta, ignore_errors=False) 
        else:
            print(f'La carpeta {carpeta} no existe')
    return True

carpetas=[
    'baunit/migrations',
    'codelist/migrations',
    'core/migrations',
    'party/migrations',
    'rrr/migrations',
    'source/migrations',
    'spatialunit/migrations',
    'ppp'
]

borrar_carpetas(carpetas)