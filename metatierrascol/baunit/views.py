# Create your views here.
#Django imports
from django.http import JsonResponse, HttpRequest

#rest framework imports
from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView



#mis módulos
from . import serializers, models
from core.commonlibs import managePermissions

class BaunitViewSet(viewsets.ModelViewSet):
    queryset = models.Baunit.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.BaunitSerializer

