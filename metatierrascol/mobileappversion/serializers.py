from django.contrib.auth.models import User
from django.db.models import Max
from rest_framework import serializers

from .models import MobileAppVersion, MobileAppVersionNotes

class MobileAppVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model=MobileAppVersion
        fields = ['id', 'version','archivo',
                   'publicar','fecha','creado_por', 'url_descarga']
        
    def validate_version(self, value):
        #si los valores son correctos, devuelve return attrs
        #si hay error return serializers.ValidationError('El mensaje')
        print ("Validando version")
        max_version = MobileAppVersion.objects.aggregate(Max('version'))['version__max']
        #max puede ser {'version__max': None}, si no hay versiones,
        # o {'version__max': 1.3} si es la versión 1.3 la mayor
        if max_version is not None:
            if max_version >= value:
                raise serializers.ValidationError(f'Existe una versión mayor o igual. Versión existente: {max_version}. Versión intentada: {value}')
        return value

class MobileAppVersionNotesSerializer(serializers.ModelSerializer):
    class Meta:
        model=MobileAppVersionNotes
        fields = ['id','mobileappversion', 'fecha', 'nota','creado_por']

