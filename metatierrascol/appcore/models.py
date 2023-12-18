from django.db import models

# Create your models here.

class AppSettings(models.Model):
    gid = models.AutoField(primary_key=True)
    parameter_name = models.CharField(unique=True, max_length=50, blank=True, null=True)
    parameter_value = models.CharField(max_length=200, blank=True, null=True)
    help_en = models.CharField(max_length=200, blank=True, null=True)
    help_es = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'settings'


class Municipio(models.Model):
    #departamento,provincia,codigo_municipio,nombre_municipio
    gid = models.AutoField(primary_key=True)
    departamento = models.CharField(unique=True, max_length=100)
    provincia = models.CharField(unique=True, max_length=100)
    codigo_municipio = models.IntegerField()
    nombre_municipio = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'municipio'