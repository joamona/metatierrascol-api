from django.contrib import admin
from appcodelist import models

# Register your models here.
class MunicipioAdmin(admin.ModelAdmin):
    list_display = ('gid','departamento','provincia','codigo_municipio','nombre_municipio')

admin.site.register(models.Municipio, MunicipioAdmin) 
