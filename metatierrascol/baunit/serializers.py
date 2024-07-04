import datetime
from django.contrib.auth.models import User

from rest_framework import serializers

from .models import Baunit
from codelist.models import Departamento, Provincia, Municipio, Lc_prediotipo, EstadoExpediente, Sector

class BaunitSerializer(serializers.ModelSerializer):
    creado_por=serializers.SlugRelatedField(queryset=User.objects.all(),slug_field='username',read_only=False, many=False,required=False)
    provincia=serializers.SlugRelatedField(queryset=Provincia.objects.all(),slug_field='provincia',read_only=False, many=False,required=True)
    departamento=serializers.SlugRelatedField(queryset=Departamento.objects.all(),slug_field='departamento',read_only=False, many=False,required=True)
    sector_predio=serializers.SlugRelatedField(queryset=Sector.objects.all(),slug_field='sector',read_only=False, many=False,required=True)
    municipio=serializers.SlugRelatedField(queryset=Municipio.objects.all(),slug_field='codigo_municipio',read_only=False, many=False,required=True)
    tipo=serializers.SlugRelatedField(queryset=Lc_prediotipo.objects.all(),slug_field='lc_prediotipo',read_only=False, many=False,required=True)
    estado_expediente=serializers.SlugRelatedField(queryset=EstadoExpediente.objects.all(),slug_field='estado_expediente',read_only=False, many=False,required=False)
    class Meta:
        model=Baunit
        fields = ['id','creado_por', 'fecha_creacion',
                   'codigo_acceso','nombre','provincia',
                   'departamento','sector_predio','municipio','numero_predial',
                   'tipo','complemento', 'estado_expediente', 'longitud', 'latitud', 'numero_catastral']

    # def create(self, validated_data):
    #     # print('validated_data')
    #     # print(validated_data)
    #     es=list(EstadoExpediente.objects.filter(estado_expediente='Recibido'))[0]
    #     ba=Baunit(**validated_data,creado_por=self.context['request'].user, estado_expediente=es)
    #     ba.save()
    #     return ba

    
