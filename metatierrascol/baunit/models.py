from django.db import models
#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from uuid import uuid4

from codelist import models as codelist_models

class Baunit(models.Model):
    id = models.AutoField(primary_key=True)
    creado_por = models.ForeignKey(get_user_model(), null=False, related_name='creado_por', on_delete=models.DO_NOTHING)#no se borra el registro
    fecha_creacion = models.DateTimeField(auto_now=True)
#    modificado_por = models.ForeignKey(get_user_model(),null=True,on_delete=models.SET_NULL, related_name='modificado_por')#no se borra el registro
#    fecha_modificacion = models.DateTimeField(null=True)
    uuid = models.UUIDField(unique=True, editable=False, default= uuid4, null=False)
    nombre = models.TextField(max_length=100)
    departamento = models.ForeignKey(codelist_models.Departamento, null=False, on_delete=models.DO_NOTHING)
    sector_predio = models.ForeignKey(codelist_models.Sector, null=False, on_delete=models.DO_NOTHING)
    municipio = models.ForeignKey(codelist_models.Municipio, null=False, on_delete=models.DO_NOTHING)
    numero_predial = models.TextField(max_length=50, null=True, unique=True)
    tipo = models.ForeignKey(codelist_models.Lc_prediotipo, null=False, on_delete=models.DO_NOTHING)
    complemento = models.TextField(max_length=200, help_text='Complemento de la dirección para ayudar a localizar el predio')
    estado_expediente = models.ForeignKey(codelist_models.EstadoExpediente, null=False, on_delete=models.DO_NOTHING) 
    class Meta:
        managed = False
        db_table = 'baunit"."baunit'

