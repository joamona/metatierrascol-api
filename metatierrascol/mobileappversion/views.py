import os

from django.db.models import Max
from django.http import FileResponse

from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer

from pgOperations.pgOperations import WhereClause, FieldsAndValues

from core.accesspolicy import generalAccessPolicy
from core.commonlibs import generalModule
from metatierrascol import settings
from . import serializers
from .models import MobileAppVersion as MobileAppVersionModel, MobileAppVersionNotes as MobileAppVersionNotesModel

#necesaro para descargar archivos
from core.commonlibs import fileRenderer 


class MobileAppVersionViewSet(viewsets.ModelViewSet):
    parser_classes = (MultiPartParser, JSONRenderer)
    queryset = MobileAppVersionModel.objects.all().order_by('version')
    serializer_class = serializers.MobileAppVersionSerializer
    permission_classes = [generalAccessPolicy.AllowAnySafeMethodsAdminPostMethods]

    def create(self, request, *args, **kwargs):
        """
        Uploads a new version of app.
        Mandatory fields:
        version: the version number. Must be biggest than the lattest one
        file: the apk file
        """
        # Serializa los datos recibidos en la solicitud       
        data=request.data.copy()#hago esto porque request.data es inmutable en la versión 4.2.7 de django
        archivo = request.FILES['archivo']
        data['archivo']=archivo
        data['creado_por']=request.user.id
        tamaño=len(archivo.file.getvalue())/1000000
        print(f'Tamaño archivo: {tamaño}')
        
        serializer = serializers.MobileAppVersionSerializer(data=data)

        if serializer.is_valid():
            ar: MobileAppVersionModel=serializer.save()
            ar.url_descarga=settings.API_URL + 'mobileappversion/mobile_app_version/download_version/' + str(ar.version) + '/'
            new_path=str(settings.MEDIA_ROOT) + '/mobileappversion/' + str(ar.version) + '.apk'
            os.rename(ar.archivo.path, new_path)
            ar.archivo.name = 'mobileappversion/' + str(ar.version) + '.apk'
            ar.save()
            return Response(
                {
                    'ok':True,
                    'message': f'Versión guardada exitosamente ({tamaño} mb). Número de versión {ar.version}', 
                    'data':[{
                        'id':ar.id, 
                        'version':ar.version,
                        'url_descarga':ar.url_descarga, 
                        'filename':ar.archivo.name,
                        'publicar':ar.publicar,'fecha':ar.fecha, 
                        'creado_por':ar.creado_por.id
                    }],
                    'error':[]
                }, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    #Si comento la línea @action ... no aparece en swagger dos veces. 
    #Esto lo añade una vez, si no lo comento:
    #    router.register(r'mobile_app_version',views.MobileAppVersionViewSet,'mobile_app_version')
    #Y luego aparecería otra vez por estar en las urls manualmente:
    #    path('mobile_app_version/download_version/<version>/',views.MobileAppVersionViewSet.as_view({'get': 'download_version'}), name='download_version'),    
    #al comentarlo solo aparece una vez
    #@action(detail=False, methods=['get'])
    def download_version(self, request, version=None):
        """
        Downloads the specified version. The parameter
        version -- The version number, not the version id.
        """ 
        self.renderer_classes=(fileRenderer.PassthroughRenderer, JSONRenderer)
        qs=self.queryset.filter(version=float(version))#cojo el queryset 
                                #de la variable de clase y le aplico otro filtro
        l=(list(qs))
        if len(l)>0:
            ar=l[0]
            filename= str(settings.MEDIA_ROOT) + '/' + ar.archivo.name

            if not(os.path.isfile(filename)):
                return Response({"Error": f"El fichero {filename} ha sido borrado"}, content_type='application/json', status=status.HTTP_404_NOT_FOUND)
 
            file_handle = ar.archivo.open()
            response = FileResponse(file_handle, content_type='.apk, application/apk, application/octet-stream')
            response['Content-Length'] = ar.archivo.size
            nombreApk='metatierrasapp_v' + str(version) + '.apk'
            response['Content-Disposition'] = 'attachment; filename="%s"' % nombreApk
            return response            
        else:
            return Response({'message':f'La versión {version} no existe'})
        

    def publicar_version(self, request, version_id=None):
        pgo = generalModule.getDjangoPg()
        whereClause = WhereClause('id=%s',[version_id])
        fieldsAndValues=FieldsAndValues({'publicar':True})
        n=pgo.pgUpdate('mobileappversion.mobileappversion',fieldsAndValues,whereClause)
        if n==1:
            return Response({'ok':[f'Numero de versiones publicadas {n}']})
        else:
            return Response({'error':[f'Numero de versiones publicadas {n}']},status=status.HTTP_400_BAD_REQUEST)
            
    def despublicar_version(self, request, version_id=None):
        pgo = generalModule.getDjangoPg()
        whereClause = WhereClause('id=%s',[version_id])
        fieldsAndValues=FieldsAndValues({'publicar':False})
        n=pgo.pgUpdate('mobileappversion.mobileappversion',fieldsAndValues,whereClause)
        if n==1:
            return Response({'ok':[f'Numero de versiones despublicadas {n}']})
        else:
            return Response({'error':[f'Numero de versiones despublicadas {n}']},status=status.HTTP_400_BAD_REQUEST)
      

    @action(detail=False, methods=['get'])
    def get_last_version_details(self, request):
        """
        Gets the latest version details
        """
        whereClause = WhereClause('publicar = %s',[True])
        pgo =generalModule.getDjangoPg()
        r=pgo.pgSelect('mobileappversion.mobileappversion',"max(version) as max_version", whereClause=whereClause)
        if r[0]['max_version'] is None:
            return Response({'error': ['No hay versiones activadas de la app todavía']})   
        else:
            whereClause = WhereClause('version = %s',[r[0]['max_version']])
            r=pgo.pgSelect('mobileappversion.mobileappversion','*',whereClause=whereClause)
            r1=generalModule.remove_id_fromDictKeys(r[0])
            return Response(r1)

class MobileAppVersionNotesViewSet(viewsets.ModelViewSet):
    #parser_classes = (MultiPartParser, JSONRenderer)
    queryset = MobileAppVersionNotesModel.objects.all()
    serializer_class = serializers.MobileAppVersionNotesSerializer
    permission_classes = [generalAccessPolicy.AllowAnySafeMethodsAdminPostMethods]

    def create(self, request, *args, **kwargs):
        """
        Añade una nueva nota a la versión
        mobileappversion: es el id de la versión, no el número de la versión
        """
        # Serializa los datos recibidos en la solicitud       
        data=request.data.copy()#hago esto porque request.data es inmutable en la versión 4.2.7 de django
        
        data['creado_por']=request.user.id
        print("----notes------")
        print(data)
        serializer=self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    #Lo comento para que no aparezca en swagger dos veces
    #@action(detail=False, methods=['get'])
    def get_version_notes(self, request, version_id=None):
        """
        version_id -- The version id, not the version number.
        """
        qs=self.queryset.filter(mobileappversion=int(version_id)).order_by('id')#cojo el queryset 
                                #de la variable de clase y le aplico otro filtro
        l=(list(qs))
        if len(l)>0:
            s=self.serializer_class(l,many=True)
            return Response(s.data)
        else:
            return Response({'error':[f'La versión id: {version_id} no tiene comentarios']},status=status.HTTP_400_BAD_REQUEST)
