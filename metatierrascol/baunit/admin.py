from django.contrib import admin
from . import models

# Register your models here.

class BaunitAdmin(admin.ModelAdmin):
    list_display = ('id','creado_por', 'fecha_creacion',
                  'uuid','nombre',
                  'departamento','sector_predio','municipio','numero_predial',
                  'tipo','complemento', 'estado_expediente')
    
admin.site.register(models.Baunit, BaunitAdmin)

