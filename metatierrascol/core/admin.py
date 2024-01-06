from django.contrib import admin
from . import models

class AppSettingsAdmin(admin.ModelAdmin):
    list_display = ('parameter_name', 'parameter_value','help_es','help_en')

admin.site.register(models.AppSettings, AppSettingsAdmin) 

