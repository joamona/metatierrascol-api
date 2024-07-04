from django.db import models

# Create your models here.

class SnrPersonaTitularTipo(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    snr_persona_titular_tipo = models.CharField(max_length=20, unique=True)
    class Meta:
        managed = False
        db_table = 'codelist"."snr_persona_titular_tipo'

class Departamento(models.Model):
    #departamento,provincia,codigo_municipio,nombre_municipio
    id = models.AutoField(primary_key=True, editable=False)
    departamento = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'codelist"."departamento'

class Provincia(models.Model):
    #departamento,provincia,codigo_municipio,nombre_municipio
    id = models.AutoField(primary_key=True, editable=False)
    provincia = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'codelist"."provincia'

class Municipio(models.Model):
    #departamento,provincia,codigo_municipio,nombre_municipio
    id = models.AutoField(primary_key=True, editable=False)
    departamento = models.CharField(max_length=100)
    provincia = models.CharField(max_length=100)
    codigo_municipio = models.IntegerField(unique=True,)
    nombre_municipio = models.CharField(max_length=100)

    class Meta:
        managed = False
        unique_together = ('codigo_municipio', 'nombre_municipio',)
        db_table = 'codelist"."municipio'


class Sector(models.Model):
    #departamento,provincia,codigo_municipio,nombre_municipio
    id = models.AutoField(primary_key=True, editable=False)
    sector = models.CharField(max_length=20, unique=True)

    class Meta:
        managed = False
        db_table = 'codelist"."sector'

class Lc_prediotipo(models.Model):
    #departamento,provincia,codigo_municipio,nombre_municipio
    id = models.AutoField(primary_key=True, editable=False)
    lc_prediotipo = models.CharField(max_length=50, unique=True)

    class Meta:
        managed = False
        db_table = 'codelist"."lc_prediotipo'

class EstadoExpediente(models.Model):
    #departamento,provincia,codigo_municipio,nombre_municipio
    id = models.AutoField(primary_key=True, editable=False)
    estado_expediente = models.CharField(max_length=50, unique=True)

    class Meta:
        managed = False
        db_table = 'codelist"."estado_expediente'