from django.db import models

# Create your models here.

class AppSettings(models.Model):
    gid = models.AutoField(primary_key=True, editable=False)
    parameter_name = models.CharField(unique=True, max_length=50, blank=True, null=True, help_text='Nombre del parámetro')
    parameter_value = models.CharField(max_length=200, blank=True, null=True)
    help_en = models.CharField(max_length=200, blank=True, null=True)
    help_es = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'core"."appsettings'
