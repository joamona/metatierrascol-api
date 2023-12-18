from django.contrib import admin
from appcore import models

class AppSettingsAdmin(admin.ModelAdmin):
    list_display = ('gid', 'parameter_name', 'parameter_value','help_es','help_en')

admin.site.register(models.AppSettings, AppSettingsAdmin) 

