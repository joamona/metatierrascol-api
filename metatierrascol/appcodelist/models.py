from django.db import models

# Create your models here.

class SnrPersonaTitularTipo(models.Model):
    gid = models.AutoField(primary_key=True)
    snr_persona_titular_tipo = models.CharField(max_length=20, unique=True)
    class Meta:
        managed = False
        db_table = 'codelist"."snr_persona_titular_tipo'

class Municipio(models.Model):
    #departamento,provincia,codigo_municipio,nombre_municipio
    gid = models.AutoField(primary_key=True)
    departamento = models.CharField(unique=True, max_length=100)
    provincia = models.CharField(unique=True, max_length=100)
    codigo_municipio = models.IntegerField()
    nombre_municipio = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'codelist"."municipio'