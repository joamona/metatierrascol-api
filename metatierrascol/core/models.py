from django.db import models
from django.contrib.auth import get_user_model

from codelist import models as codelist_models

# Create your models here.


class AppSettings(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    parameter_name = models.CharField(unique=True, max_length=50, blank=True, null=True, help_text='Nombre del parámetro')
    parameter_value = models.CharField(max_length=200, blank=True, null=True)
    help_en = models.CharField(max_length=200, blank=True, null=True)
    help_es = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'core"."appsettings'


class AccesoMunicipio(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    user = models.ForeignKey(get_user_model(),  related_name='accesoMunicipio_user_id', on_delete=models.DO_NOTHING)#no se borra el registro
    municipio = models.ForeignKey(codelist_models.Municipio, on_delete=models.DO_NOTHING,blank = False)
    class Meta:
        managed = False
        db_table = 'core"."acceso_municipio'


class UsuariosAvisadosDescargaZip(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    user = models.ForeignKey(get_user_model(),  related_name='usuariosAvisadosDescargaZip_user_id', on_delete=models.DO_NOTHING)#no se borra el registro
    class Meta:
        managed = False
        db_table = 'core"."usuarios_avisados_descarga_zip'