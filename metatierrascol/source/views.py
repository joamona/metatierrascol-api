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
from rest_framework.renderers import JSONRenderer

from pgOperations.pgOperations import WhereClause

from metatierrascol import settings
from . import serializers
from .models import ArchivoZip as ArchivoZipModel
from baunit.serializers import BaunitSerializer
from core.commonlibs import generalModule
from core.accesspolicy import generalAccessPolicy
from core.commonlibs import fileRenderer #necesaro para descargar archivos
from core.commonlibs import emails

#ESTO FUNCIONABA, PERO YA NO SE USA. AHORA USO UNA VISTA MODELVIEWSET
#las vistas de clase normales también requieren el token
# class AñadeFicheroZip(View):
#     def post(self, request):
#         r=manageFiles.uploadFile(request)
#         return JsonResponse(r)

# class PassthroughRenderer(renderers.BaseRenderer):
#     """
#         Return data as-is. View should supply a Response.
#     """
#     media_type = ''
#     format = ''
#     def render(self, data, accepted_media_type=None, renderer_context=None):
#         return data

class ArchivoZip(viewsets.ModelViewSet):
    """
    Crea una baunit, y luego crea el fichero asociado
    """


    parser_classes = (MultiPartParser, JSONRenderer)
    queryset = ArchivoZipModel.objects.all()
    serializer_class = serializers.ArchivoZipSerializer
    permission_classes = (generalAccessPolicy.Allow_AuthenticatedSafeMethodsAndPostMethods,)

    def create(self, request, *args, **kwargs):
        # Serializa los datos recibidos en la solicitud       
        data=request.data.copy()#hago esto porque request.data es inmutable en la versión 4.2.7 de django
        data['estado_expediente']='Recibido'
        data['creado_por']=request.user
        sbaunit=BaunitSerializer(data=data)
        if sbaunit.is_valid():
            #print('Es valido')
            baunit=sbaunit.save()
        else:
            #print('s.errors')
            return Response(sbaunit.errors)
        #print(data)
        #print(request.data)
        #print(request.FILES)
        archivo = request.FILES['archivo']
        tamaño=len(archivo.file.getvalue())/1000000
        #print(f'Tamaño archivo: {tamaño}')
        archivo.filename=str(baunit.id) + '.zip'
        data['archivo']=archivo
        data['baunit']=baunit.id
        data['creado_por']=request.user.id
        serializer = serializers.ArchivoZipSerializer(data=data)

        if serializer.is_valid():
            ar=serializer.save()
            ar.url_descarga=settings.API_URL + 'source/descarga_zip_codigo_acceso/' + str(baunit.codigo_acceso) + '/'
            ar.save()
            borrar=generalModule.getSetting('borrar_fichero_zip_al_descargar')
            if borrar.lower() == 'true':
                mensaje = 'Por seguridad, el fichero SERÁ ELIMINADO después de la primera descarga'
            else:
                mensaje = 'Por seguridad, el fichero NO será eliminado después de la primera descarga'
            # Esta setting ha sido eliminada
            # if settings.DJANGO_SEND_EMAIL_ON_FILE_UPLOAD:
            #    avisaZipDisponibleDescarga(str(baunit.codigo_acceso), request.user.username, tamaño,data)

            if generalModule.getSetting('enviar_email_cuando_un_usuario_sube_un_predio').lower()=="true":
                emails.avisaZipDisponibleDescarga(str(baunit.codigo_acceso), request.user.username, tamaño,data)
            
            return Response({'mensaje': f'Archivo y datos guardados exitosamente ({tamaño} mb). Los usuarios han sido avisados para la descarga. {mensaje}'}, status=status.HTTP_201_CREATED)
            # try:
            #     pass
            #     # ar=serializer.save()
            #     # ar.url_descarga=settings.API_URL + 'source/descarga_zip_codigo_acceso/' + str(baunit.codigo_acceso) + '/'
            #     # ar.save()
            #     # borrar=generalModule.getSetting('borrar_fichero_zip_al_descargar')
            #     # if borrar.lower() == 'true':
            #     #     mensaje = 'Por seguridad, el fichero SERÁ ELIMINADO después de la primera descarga'
            #     # else:
            #     #     mensaje = 'Por seguridad, el fichero NO será eliminado después de la primera descarga'
            #     # if settings.DJANGO_SEND_EMAIL_ON_FILE_UPLOAD:
            #     #     avisaZipDisponibleDescarga(str(baunit.codigo_acceso), request.user.username, tamaño,data)
            #     # return Response({'mensaje': f'Archivo y datos guardados exitosamente ({tamaño} mb). Los usuarios han sido avisados para la descarga. {mensaje}'}, status=status.HTTP_201_CREATED)
            # except Exception as e:
            #     print(e)
            #     return Response({'error': f'Error al guardar el archivo y los datos: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# from django.http import FileResponse
# from rest_framework import viewsets, renderers
# from rest_framework.decorators import action


class DescargaArchivoZipCodigoAcceso(views.APIView):
    renderer_classes=(fileRenderer.PassthroughRenderer, JSONRenderer)
    permission_classes = (generalAccessPolicy.AllowAny,)
    def get(self, request, codigo_acceso):
        pgo=generalModule.getDjangoPg()
        wc=WhereClause(where_clause='codigo_acceso=%s', where_values_list=[codigo_acceso])
        r=pgo.pgSelect(table_name='baunit.baunit',string_fields_to_select='id',
                     whereClause=wc)
        if len(r) > 0:
            baunit_id=r[0]['id']
            zip: ArchivoZipModel = list(ArchivoZipModel.objects.filter(baunit=baunit_id))[0]
            ar= str(settings.MEDIA_ROOT) + '/' + zip.archivo.name

            if not(os.path.isfile(ar)):
                return Response('{"Error":"El fichero ha sido borrado"}', content_type='application/json', status=status.HTTP_404_NOT_FOUND)
 
            file_handle = zip.archivo.open()
            # send file
            response = FileResponse(file_handle, content_type='.zip, application/zip, application/octet-stream')
            response['Content-Length'] = zip.archivo.size
            response['Content-Disposition'] = 'attachment; filename="%s"' % zip.archivo.name
            
            borrar=generalModule.getSetting('borrar_fichero_zip_al_descargar')
            if borrar.lower() == 'true':
                os.remove(ar)
            return response
        else:
            return Response('{"Error":"Codigo no encontrado"}',content_type='application/json', status=status.HTTP_404_NOT_FOUND)
 



