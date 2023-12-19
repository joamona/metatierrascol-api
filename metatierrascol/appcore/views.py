# Create your views here.
#Django imports
from django.http import JsonResponse, HttpResponse, HttpRequest
from django.views import View
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

#rest framework imports
from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
from django_filters import rest_framework as filters

#mis módulos
from . import serializers, models

def notLoggedIn(request: HttpRequest):
    return JsonResponse({"ok":False,"message": "You are not logged in", "data":[]})

class Index(View):
    def get(self, request):
        return JsonResponse({"ok":True,"message": "Hello world", "data":[]})


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class AppSettingsViewSet(viewsets.ModelViewSet):
    queryset = models.AppSettings.objects.all()
    permission_classes = [permissions.IsAdminUser]
    serializer_class = serializers.AppSettingsSerializer

class AppSettingsList(viewsets.ModelViewSet):
    queryset = models.AppSettings.objects.all()#el queriset trabaja con todos los obj
						#es una variable de clase
    serializer_class = serializers.AppSettingsSerializer #es una variable de clase
    permission_classes = [permissions.IsAdminUser]#esto permite a todos los métodos ser usados, 
        #pero cada método puede tener unos permisos diferentes con el siguiente decorador:
        # @action(detail=True, methods=['post'], permission_classes=[IsAdminOrIsSelf])
        #       detail=True significa que trabaje con varios registros
    def retrieve(self, request, gid=None):#fíjate que recibe request y un paraámertro de la url
        #print(self.basename, self.action, self.detail, self.suffix, self.name, self.description)
        qs2=self.queryset.filter(gid__lt=gid)#cojo el queryset de la variable de clase y le aplico
			#el filtro gid < the_gid. → lt significa less than
        s = self.get_serializer(qs2, many=True)#obtiene el serializer de la clase
			#many significa que puede trabajar
			#con varios registros, no solo uno
        return Response(s.data)