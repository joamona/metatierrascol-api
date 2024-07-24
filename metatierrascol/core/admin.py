from django.contrib import admin
from . import models

class AppSettingsAdmin(admin.ModelAdmin):
    list_display = ('parameter_name', 'parameter_value','help_es','help_en')

class AccesoMunicipioAdmin(admin.ModelAdmin):
    list_display = ('user', 'municipio')

#class UsuariosAvisadosDescargaZipAdmin(admin.ModelAdmin):
#    list_display = ('user',)

class AppUserAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'data_acceptation', 'notification_acceptation', 'interest',
                    'email_confirm_token', 'email_confirmed')
    
class CustomPasswordResetAdmin(admin.ModelAdmin):
    list_display = ('id', 'email','token', 'created_at')

admin.site.register(models.AppSettings, AppSettingsAdmin) 
admin.site.register(models.AccesoMunicipio, AccesoMunicipioAdmin) 
#admin.site.register(models.UsuariosAvisadosDescargaZip, UsuariosAvisadosDescargaZipAdmin) 
admin.site.register(models.AppUser, AppUserAdmin) 
admin.site.register(models.CustomPasswordReset, CustomPasswordResetAdmin) 

