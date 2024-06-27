# Create your views here.
#Django imports
from django.http import JsonResponse, HttpRequest
from django.contrib.auth import login

#rest framework imports
from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes

from knox.views import LoginView as KnoxLoginView
from knox.auth import TokenAuthentication


#mis módulos
from . import serializers, models
from .commonlibs import managePermissions
from .accesspolicy import generalAccessPolicy
from core.commonlibs import generalModule

def notLoggedIn(request: HttpRequest):
    return JsonResponse({"ok":False,"message": "You are not logged in", "data":[]})

@api_view(http_method_names=['GET'])
@permission_classes((permissions.AllowAny,))
def helloWorld(request):
    return Response({"ok":True,"message": "Hello world", "data":[]})

@api_view(http_method_names=['GET'])
@permission_classes((permissions.IsAuthenticated,))
def isValidToken(request):
    token = request.META.get('HTTP_AUTHORIZATION', False)
    if token:
        token = str(token).split()[1].encode("utf-8")
        knoxAuth = TokenAuthentication()
        user, auth_token = knoxAuth.authenticate_credentials(token)
        groups = managePermissions.getUserGroups_fromUsername(user.username)
        return Response({"detail": "Token Válido.", "username": user.username,
                    "groups":groups})
    else: 
        return Response({'error':'Token no encontrado'}, status=status.HTTP_400_BAD_REQUEST)

class LoginViewWithKnox(KnoxLoginView):
    """
    Login con usuario y contraseña.
    """
    permission_classes = (AllowAny, )
    serializer_class = serializers.LoginViewWithKnoxSerializer

    def post(self, request, format=None):
        """
        This text is the description for this API.
        ---
        parameters:
        - name: username
        description: El nombre del usuario
        required: true
        type: string
        paramType: form
        - name: password
        description: Contraseña
        paramType: form
        required: true
        type: string
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            login(request, user)
            response = super().post(request, format=None)
        else:
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        #print('Validated data')
        #print(serializer.validated_data)
        v=response.data #the response with the authentication token
        groups = managePermissions.getUserGroups_fromUsername(request.data['username'])
        v['groups'] = groups #la lista de grupos a los que pertenece el usuario
        v['username'] = request.data['username']
        os=generalModule.getOpenedKnoxSessions(request.data['username'])
        v['opened_sessions']= os
        return Response(v, status=status.HTTP_200_OK)

class AppSettingsViewSet(viewsets.ModelViewSet):
    queryset = models.AppSettings.objects.all()
    permission_classes = (generalAccessPolicy.AllowAuthenticatedSafeMethodsAdminPostMethods,)
    serializer_class = serializers.AppSettingsSerializer

class AppSettingsList(viewsets.ModelViewSet):
    queryset = models.AppSettings.objects.all()#el queriset trabaja con todos los obj
						#es una variable de clase
    serializer_class = serializers.AppSettingsSerializer #es una variable de clase
    permission_classes = (generalAccessPolicy.AllowAuthenticatedSafeMethods,)#esto permite 
        #a todos los métodos ser usados, 
        #pero cada método puede tener unos permisos diferentes con el siguiente decorador:
        # @action(detail=True, methods=['post'], permission_classes=[IsAdminOrIsSelf])
        #       detail=True significa que trabaje con varios registros
    def retrieve(self, request, id=None):#fíjate que recibe request y un paraámertro de la url
        #print(self.basename, self.action, self.detail, self.suffix, self.name, self.description)
        qs2=self.queryset.filter(id__lt=id)#cojo el queryset de la variable de clase y le aplico
			#el filtro gid < the_gid. → lt significa less than
        s = self.get_serializer(qs2, many=True)#obtiene el serializer de la clase
			#many significa que puede trabajar
			#con varios registros, no solo uno
        return Response(s.data)
    

class AppSettingsListQuery(generics.ListAPIView):
    """
    Esta vista se puede consultar con: 
        http://localhost:8000/core/appsettings_list_query/?help_es=a&help_es=b
    """
    queryset = models.AppSettings.objects.all()
    serializer_class = serializers.AppSettingsSerializer #
    permission_classes = [permissions.AllowAny]
    filterset_fields = ['help_es', 'help_en']

class UsuariosAvisadosDescargaZipViewSet(viewsets.ModelViewSet):
    queryset = models.UsuariosAvisadosDescargaZip.objects.all()
    permission_classes = (generalAccessPolicy.AllowAuthenticatedSafeMethodsAdminPostMethods,)
    serializer_class = serializers.UsuariosAvisadosDescargaZipSerializer