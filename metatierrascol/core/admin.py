from django.contrib import admin
from . import models

class AppSettingsAdmin(admin.ModelAdmin):
    list_display = ('parameter_name', 'parameter_value','help_es','help_en')

class AccesoMunicipioAdmin(admin.ModelAdmin):
    list_display = ('user', 'municipio')

class UsuariosAvisadosDescargaZipAdmin(admin.ModelAdmin):
    list_display = ('user',)


admin.site.register(models.AppSettings, AppSettingsAdmin) 
admin.site.register(models.AccesoMunicipio, AccesoMunicipioAdmin) 
admin.site.register(models.UsuariosAvisadosDescargaZip, UsuariosAvisadosDescargaZipAdmin) 

