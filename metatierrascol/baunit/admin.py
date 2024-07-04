from django.contrib import admin
from . import models

# Register your models here.

class BaunitAdmin(admin.ModelAdmin):
    list_display = ('id','creado_por', 'fecha_creacion',
                  'codigo_acceso','nombre',
                  'departamento','provincia','sector_predio','municipio','numero_predial',
                  'tipo','complemento', 'estado_expediente','longitud', 'latitud', 'numero_catastral')
    
admin.site.register(models.Baunit, BaunitAdmin)

