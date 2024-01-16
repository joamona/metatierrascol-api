from django.contrib import admin
from . import models
class ArchivoZipAdmin(admin.ModelAdmin):
    list_display = ('id', 'baunit_id', 'creado_por_id', 'fecha_creacion', 
                    'descargado_por_id', 'fecha_descarga', 'archivo', 'url_descarga')
    
admin.site.register(models.ArchivoZip, ArchivoZipAdmin)
