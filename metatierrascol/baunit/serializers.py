from django.utils.timezone import datetime

from django.contrib.auth import authenticate

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from . import models
from codelist.models import Municipio

class BaunitSerializer(serializers.ModelSerializer):
    #read_only_fields = ['creado_por', 'modificado_por', 'fecha_creacion','fecha_modificacion', 'gid', 'uuid']
    municipio=serializers.SlugRelatedField(queryset=Municipio.objects.all(),slug_field='nombre_municipio',read_only=False, many=False,allow_null=False)
    
    class Meta:
        model = models.Baunit
        fields = ['id','creado_por', 'fecha_creacion',
                  'uuid','nombre',
                  'departamento','sector_predio','municipio','numero_predial',
                  'tipo','complemento', 'estado_expediente']

    def create(self, validated_data):
        validated_data['fecha_modificacion']=None
        print("Validated_data")
        print(validated_data)
        ba=models.Baunit(**validated_data,creado_por=self.context['request'].user)
        ba.save()
        return ba

    # def update(self, instance, validated_data):
    #     print('Updating')
    #     instance.modificado_por = self.context['request'].user
    #     instance.fecha_modificacion = datetime.now()
    #     instance.save()
    #     return instance
