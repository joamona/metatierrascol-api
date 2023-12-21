from django.contrib.auth.models import User
from . import models
from rest_framework import serializers

class SnrPersonaTitularTipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SnrPersonaTitularTipo
        fields = '__all__'

class DepartamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Departamento
        fields = '__all__'

class ProvinciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Provincia
        fields = '__all__'

class MunicipioSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Municipio
        fields = '__all__'