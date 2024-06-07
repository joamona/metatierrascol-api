from django.db import models
from django.contrib.auth import get_user_model

class MobileAppVersion(models.Model):
    id = models.AutoField(primary_key=True)
    version = models.FloatField(unique=True)
    archivo = models.FileField(upload_to='mobileappversion')
    publicar = models.BooleanField(default=False)#valor por defecto
    fecha = models.DateTimeField(auto_now=True)
    creado_por = models.ForeignKey(get_user_model(),blank = False,  
                                   related_name='mobileappversion_creado_por', on_delete=models.DO_NOTHING)
    url_descarga = models.TextField(max_length='200', blank=True)
    class Meta:
        managed = False
        db_table = 'mobileappversion"."mobileappversion'

class MobileAppVersionNotes(models.Model):
    id = models.AutoField(primary_key=True)
    mobileappversion = models.ForeignKey(MobileAppVersion, on_delete=models.DO_NOTHING,blank = False)
    fecha = models.DateTimeField(auto_now=True)
    nota =models.CharField(max_length=2000)
    creado_por = models.ForeignKey(get_user_model(),blank = True,  
                                   related_name='mobileappversionnotes_creado_por', on_delete=models.DO_NOTHING)
    class Meta:
        managed = False
        db_table = 'mobileappversion"."mobileappversionnotes'
