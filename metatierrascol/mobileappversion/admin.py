from django.contrib import admin
from . import models

models.MobileAppVersion
models.MobileAppVersionNotes

# Register your models here.
class MobileAppVersionAdmin(admin.ModelAdmin):
    list_display =  ('id', 'version','archivo',
                   'publicar','fecha','creado_por', 'url_descarga')
    
class MobileAppVersionNotesAdmin(admin.ModelAdmin):
    list_display = ('id','mobileappversion', 'fecha', 'nota','creado_por')


admin.site.register(models.MobileAppVersion, MobileAppVersionAdmin) 
admin.site.register(models.MobileAppVersionNotes, MobileAppVersionNotesAdmin) 

