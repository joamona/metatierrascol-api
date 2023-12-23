from django.db import models
#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from uuid import uuid4

from codelist import models as codelist_models

class Baunit(models.Model):
    gid = models.AutoField(primary_key=True)
    creado_por = models.ForeignKey(get_user_model(), null=True, on_delete=models.SET_NULL, related_name='creado_por')#no se borra el registro
    fecha_creacion = models.DateTimeField(auto_now=True)
#    modificado_por = models.ForeignKey(get_user_model(),null=True,on_delete=models.SET_NULL, related_name='modificado_por')#no se borra el registro
#    fecha_modificacion = models.DateTimeField(null=True)
    uuid = models.UUIDField(unique=True, editable=False, default= uuid4, null=False)
    nombre = models.TextField(max_length=100)
    departamento = models.ForeignKey(codelist_models.Departamento, on_delete=models.CASCADE, null=False)
    sector_predio = models.ForeignKey(codelist_models.Sector,on_delete=models.CASCADE, null=False)
    municipio = models.ForeignKey(codelist_models.Municipio,on_delete=models.CASCADE, null=False)
    numero_predial = models.TextField(max_length=50, null=True, unique=True)
    tipo = models.ForeignKey(codelist_models.Lc_prediotipo, on_delete=models.CASCADE, null=False)
    complemento = models.TextField(max_length=200, help_text='Complemento de la dirección para ayudar a localizar el predio')
    
    class Meta:
        managed = True
        db_table = 'baunit"."baunit'

