from django.contrib import admin
from appcodelist import models

# Register your models here.

class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ('gid','departamento')

class ProvinciaAdmin(admin.ModelAdmin):
    list_display = ('gid','provincia')

class MunicipioAdmin(admin.ModelAdmin):
    list_display = ('gid','departamento','provincia','codigo_municipio','nombre_municipio')

admin.site.register(models.Departamento, DepartamentoAdmin) 
admin.site.register(models.Provincia, ProvinciaAdmin) 
admin.site.register(models.Municipio, MunicipioAdmin) 
