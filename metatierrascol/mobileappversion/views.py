import os, sys

from django.core.mail import send_mail
from django.http import FileResponse

from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import views
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.renderers import JSONRenderer

from pgOperations.pgOperations import WhereClause

from metatierrascol import settings
from . import serializers
from .models import MobileAppVersion as MobileAppVersionModel, MobileAppVersionNotes as MobileAppVersionNotesModel
from core.commonlibs import generalModule
from core.accesspolicy import generalAccessPolicy
from core.commonlibs import fileRenderer #necesaro para descargar archivos

class MobileAppVersionViewSet(viewsets.ModelViewSet):
    parser_classes = (MultiPartParser, JSONRenderer)
    queryset = MobileAppVersionModel.objects.all()
    serializer_class = serializers.MobileAppVersionSerializer
    permission_classes = [generalAccessPolicy.AllowAuthenticatedSafeMethodsAdminPostMethods]

    def create(self, request, *args, **kwargs):
        # Serializa los datos recibidos en la solicitud       
        data=request.data.copy()#hago esto porque request.data es inmutable en la versión 4.2.7 de django
        archivo = request.FILES['archivo']
        data['archivo']=archivo
        data['creado_por']=request.user.id
        tamaño=len(archivo.file.getvalue())/1000000
        print(f'Tamaño archivo: {tamaño}')
        #archivo.filename=str('version_' + data['version']) + '.apk'
        serializer = serializers.MobileAppVersionSerializer(data=data)

        if serializer.is_valid():
            ar=serializer.save()
            ar.url_descarga=settings.API_URL + 'mobileappversion/mobile_app_version/' + str(ar.id) + '/'
            ar.save()
            #if settings.DJANGO_SEND_EMAIL_ON_FILE_UPLOAD:
            #    avisaZipDisponibleDescarga(str(baunit.codigo_acceso), request.user.username, tamaño,data)
            return Response({'mensaje': f'Versión guardada exitosamente ({tamaño} mb).'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

