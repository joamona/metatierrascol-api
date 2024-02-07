from django.db import models
#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from uuid import uuid4

from codelist import models as codelist_models

#MARCO LOS CAMPOS NO REQUERIDOS DESDE EL PUNTO DE VISTA DEL USUARIO
#MUCHOS MÁS CAMPOS SON REQUERIDOS POR LA BASE DE DATOS,
#ESTOS CAMPOS SON RELLENADOS AUTOMÁTICAMENTE POR EL SERIALIZADOR
#PERO YA SE ENCARGA LA BASE DE DATOS DE RECHAZAR LAS FILAS CON FALTA DE DATOS
#NO ES NECESARIO ESPECIFICAR AQUÍ LOS CAMPOS REQUERIDOS POR LA BBDD

#-------------------------------------------------
#EN LOS MODELOS:
#   campos NOrequeridos se marcan con ,blank = True
#   campos requeridos se marcan con ,blank = False (defecto)
#EN LOS SERIALIZADORES:
#   Los campos requeridos para el usuario en el serializador se marcan com required=True (Defecto)
#-------------------------------------------------


class Baunit(models.Model):
    id = models.AutoField(primary_key=True)
    creado_por = models.ForeignKey(get_user_model(),blank = True,  related_name='creado_por', on_delete=models.DO_NOTHING)#no se borra el registro
    fecha_creacion = models.DateTimeField(auto_now=True,blank = True)
#    modificado_por = models.ForeignKey(get_user_model(),null=True,on_delete=models.SET_NULL, related_name='modificado_por')#no se borra el registro
#    fecha_modificacion = models.DateTimeField(null=True)
    codigo_acceso = models.UUIDField(blank = True,unique=True, editable=False, default= uuid4)
    nombre = models.TextField(max_length=100, blank = False)
    departamento = models.ForeignKey(codelist_models.Departamento, on_delete=models.DO_NOTHING,blank = False)
    provincia = models.ForeignKey(codelist_models.Provincia, on_delete=models.DO_NOTHING,blank = False)
    sector_predio = models.ForeignKey(codelist_models.Sector, on_delete=models.DO_NOTHING,blank = False)
    municipio = models.ForeignKey(codelist_models.Municipio, on_delete=models.DO_NOTHING,blank = False)
    numero_predial = models.TextField(blank = True,max_length=50)
    tipo = models.ForeignKey(codelist_models.Lc_prediotipo, on_delete=models.DO_NOTHING,blank = False)
    complemento = models.TextField(blank = False, max_length=200,  help_text='Complemento de la dirección para ayudar a localizar el predio')
    estado_expediente = models.ForeignKey(codelist_models.EstadoExpediente, on_delete=models.DO_NOTHING, blank = True) 
    longitud = models.FloatField(blank=True,help_text="Longitud del punto central del predio")
    latitud = models.FloatField(blank=True,help_text="Latitud del punto central del predio")
    numero_catastral = models.TextField(max_length=30, blank = True)
    class Meta:
        managed = False
        db_table = 'baunit"."baunit'

