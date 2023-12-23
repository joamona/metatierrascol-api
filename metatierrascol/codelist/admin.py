from django.contrib import admin
from . import models

# Register your models here.

class SnrPersonaTitularTipoAdmin(admin.ModelAdmin):
    list_display = ('id','snrpersonatitulartipo')

class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ('id','departamento')

class ProvinciaAdmin(admin.ModelAdmin):
    list_display = ('id','provincia')

class MunicipioAdmin(admin.ModelAdmin):
    list_display = ('id','departamento','provincia','codigo_municipio','nombre_municipio')

class SectorAdmin(admin.ModelAdmin):
    list_display=('id','sector')

class Lc_prediotipoTipoAdmin(admin.ModelAdmin):
    list_display=('id','lc_prediotipo')

class EstadoExpedienteTipoAdmin(admin.ModelAdmin):
    list_display=('id','estado_expediente')

admin.site.register(models.Departamento, DepartamentoAdmin) 
admin.site.register(models.Provincia, ProvinciaAdmin) 
admin.site.register(models.Municipio, MunicipioAdmin) 
admin.site.register(models.Sector, SectorAdmin) 
admin.site.register(models.Lc_prediotipo, Lc_prediotipoTipoAdmin) 
admin.site.register(models.EstadoExpediente, EstadoExpedienteTipoAdmin) 
