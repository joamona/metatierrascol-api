from django.contrib.auth.models import User
from rest_framework import serializers

from .models import MobileAppVersion, MobileAppVersionNotes

class MobileAppVersionSerializer(serializers.ModelSerializer):
    #creado_por=serializers.SlugRelatedField(queryset=User.objects.all(),slug_field='username',read_only=False, many=False,required=False)

    class Meta:
        model=MobileAppVersion
        fields = ['id', 'archivo',
                   'publicar','fecha','creado_por', 'url_descarga']

class MobileAppVersionNotesSerializer(serializers.ModelSerializer):
    creado_por=serializers.SlugRelatedField(queryset=User.objects.all(),slug_field='username',read_only=False, many=False,required=False)
    class Meta:
        model=MobileAppVersionNotes
        fields = ['id','mobileappversion', 'fecha',
                   'nota','creado_por']

