# Create your views here.
#Django imports
from django.http import JsonResponse, HttpRequest

#rest framework imports
from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes

#mis módulos
from . import serializers, models
from core.commonlibs import managePermissions

from django.db.models.query import prefetch_related_objects
from codelist.models import EstadoExpediente

class BaunitViewSet(viewsets.ModelViewSet):
    queryset = models.Baunit.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.BaunitSerializer

    def create(self, request, *args, **kwargs):
        data=request.data.copy()
        data['estado_expediente']='Recibido'
        data['creado_por']=request.user
        serializer=serializers.BaunitSerializer(data=data)
        #Esto funcionaba
        #   r=super().create(request, *args, **kwargs)
        #   return r
        #pero lo he cambiado por lo que hay abajo
        if serializer.is_valid():
            try:
                serializer.save()
                return Response({'mensaje': 'Datos guardados exitosamente.', 'elemento':serializer.data}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': f'Error al guardar los datos: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
 
    def update(self, request, *args, **kwargs):
        data=request.data.copy()
        data['creado_por']=request.user
        o=self.get_object()
        serializer=serializers.BaunitSerializer(instance=o,data=data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response({'mensaje': 'Datos actualizados exitosamente.', 'elemento':serializer.data}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': f'Error al actualizar los datos: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
