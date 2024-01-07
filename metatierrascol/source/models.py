from django.db import models
from django.contrib.auth import get_user_model

from baunit import models as baunit_models

class FicheroZip(models.Model):
    id = models.AutoField(primary_key=True)
    baunit = models.ForeignKey(baunit_models.Baunit, on_delete=models.DO_NOTHING,blank = False)
    creado_por = models.ForeignKey(get_user_model(), related_name='fichero_zip_creado_por', on_delete=models.DO_NOTHING)#no se borra el registro
    fecha_creacion = models.DateTimeField(auto_now=True)
    descargado_por = models.ForeignKey(get_user_model(), blank=True, related_name='descargado_por', on_delete=models.DO_NOTHING)#no se borra el registro
    fecha_descarga = models.DateTimeField(blank = True)
    nombre_fichero = models.FileField(upload_to='ficheros_zip')
    class Meta:
        managed = False
        db_table = 'source"."fichero_zip'
