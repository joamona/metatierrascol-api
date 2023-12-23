from django.contrib import admin
from . import models

# Register your models here.

class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ('gid','departamento')

class ProvinciaAdmin(admin.ModelAdmin):
    list_display = ('gid','provincia')

class MunicipioAdmin(admin.ModelAdmin):
    list_display = ('gid','departamento','provincia','codigo_municipio','nombre_municipio')

class SectorAdmin(admin.ModelAdmin):
    list_display=('gid','sector')

class Lc_prediotipoTipoAdmin(admin.ModelAdmin):
    list_display=('gid','lc_prediotipo')


admin.site.register(models.Departamento, DepartamentoAdmin) 
admin.site.register(models.Provincia, ProvinciaAdmin) 
admin.site.register(models.Municipio, MunicipioAdmin) 
admin.site.register(models.Sector, SectorAdmin) 
admin.site.register(models.Lc_prediotipo, Lc_prediotipoTipoAdmin) 
