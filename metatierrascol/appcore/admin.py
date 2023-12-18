from django.contrib import admin
from appcore import models

class AppSettingsAdmin(admin.ModelAdmin):
    list_display = ('gid', 'parameter_name', 'parameter_value','help_es','help_en')

class MunicipioAdmin(admin.ModelAdmin):
    list_display = ('gid','departamento','provincia','codigo_municipio','nombre_municipio')

admin.site.register(models.AppSettings, AppSettingsAdmin) 
admin.site.register(models.Municipio, MunicipioAdmin) 
