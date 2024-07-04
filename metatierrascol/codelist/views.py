#Django imports
from django.shortcuts import render

#rest framework imports
from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
from django_filters import rest_framework as filters

#local imports
from . import models, serializers

# Create your views here.

class SnrPersonaTitularTipoViewSet(viewsets.ModelViewSet):
    queryset = models.SnrPersonaTitularTipo.objects.all()
    permission_classes = [permissions.IsAdminUser]
    serializer_class = serializers.SnrPersonaTitularTipoSerializer

class DepartamentoViewSet(viewsets.ModelViewSet):
    queryset = models.Departamento.objects.all()
    permission_classes = [permissions.IsAdminUser]
    serializer_class = serializers.DepartamentoSerializer

class ProvinciaViewSet(viewsets.ModelViewSet):
    queryset = models.Provincia.objects.all()
    permission_classes = [permissions.IsAdminUser]
    serializer_class = serializers.ProvinciaSerializer

class MunicipioViewSet(viewsets.ModelViewSet):
    queryset = models.Municipio.objects.all()
    permission_classes = [permissions.IsAdminUser]
    serializer_class = serializers.MunicipioSerializer
