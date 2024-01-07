from django.contrib import admin
from . import models
class FicheroZipAdmin(admin.ModelAdmin):
    list_display = ('id', 'baunit_id', 'creado_por_id', 'fecha_creacion', 
                    'descargado_por_id', 'fecha_descarga', 'nombre_fichero')
    
admin.site.register(models.FicheroZip, FicheroZipAdmin)
