from django.contrib import admin
from . import models

# Register your models here.

class BaunitAdmin(admin.ModelAdmin):
    list_display = ('gid','creado_por','fecha_creacion','modificado_por','fecha_modificacion','uuid',
                    'nombre','get_departamento','departamento','sector_predio','municipio','numero_predial',
                    'tipo')

    def get_departamento(self, instance):
        return instance.departamento.departamento
    
admin.site.register(models.Baunit, BaunitAdmin)

