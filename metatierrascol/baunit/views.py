# Create your views here.
#Django imports
from django.http import JsonResponse, HttpRequest

#rest framework imports
from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
#mis módulos
from . import serializers, models
from core.commonlibs import managePermissions

from django.db.models.query import prefetch_related_objects
from codelist.models import EstadoExpediente
from . import accessPolicy

from core.commonlibs import generalModule

numero_maximo_de_filas_recuperadas = int(generalModule.getSetting('numero_maximo_de_filas_recuperadas'))

class BaunitViewSet(viewsets.ModelViewSet):
    queryset = models.Baunit.objects.all().order_by('fecha_creacion')[:numero_maximo_de_filas_recuperadas]
    permission_classes = (accessPolicy.BaunitViewSetAccessPolicy,)
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
        
    @action(detail=False, methods=['post'])
    def get_created_by_user_baunits(self, request, *args, **kwargs):
        """
        Gets the baunits created by a user
        Needs the creado_por by post
        """
        creado_por = request.data.get('creado_por','')

        if creado_por == '':
            return Response({'error': ['El campo creado_por no ha sido enviado']})
        
        l=generalModule.getUserModelFromUsername(creado_por)
        if len(l) == 0:
            return Response({'error': [f'El usuario {creado_por} no existe' ]})
        
        self.queryset=models.Baunit.objects.filter(creado_por=l[0].id).order_by('fecha_creacion')[:numero_maximo_de_filas_recuperadas]
        s = self.get_serializer(self.queryset, many=True)
        return Response(s.data)

