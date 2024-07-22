# Create your views here.
#Django imports
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.template.loader import get_template


#rest framework imports
from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, action

from knox.views import LoginView as KnoxLoginView
from knox.auth import TokenAuthentication

from pgOperations.pgOperations import FieldsAndValues, WhereClause

#mis módulos
from . import serializers, models
from .commonlibs import managePermissions
from .accesspolicy import generalAccessPolicy
from core.commonlibs import generalModule
from core.commonlibs import captchaModule
from core.commonlibs import emails, tokens
from metatierrascol import settings

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
        os=generalModule.getOpenedKnoxSessions(user.username)
        return Response({"detail": "Token Válido.", "username": user.username,
                    "groups":groups, "opened_sessions":os})
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

#class UsuariosAvisadosDescargaZipViewSet(viewsets.ModelViewSet):
#    queryset = models.UsuariosAvisadosDescargaZip.objects.all()
#    permission_classes = (generalAccessPolicy.AllowAuthenticatedSafeMethodsAdminPostMethods,)
#    serializer_class = serializers.UsuariosAvisadosDescargaZipSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = (generalAccessPolicy.AllowAnyCreate_AdminRestOfOperations,)

    def create(self, request, *args, **kwargs):
        """
        Añade una nueva nota a la versión
        mobileappversion: es el id de la versión, no el número de la versión
        """
        # Serializa los datos recibidos en la solicitud       
        data=request.data.copy()#hago esto porque request.data es inmutable en la versión 4.2.7 de django

        dCaptcha={}
        dCaptcha['captcha_0']=data['captcha_0']
        dCaptcha['captcha_1']=data['captcha_1']
        acierto=captchaModule.checkCaptchaFunction(dCaptcha)
        if not(acierto):
            return Response({"error": ["Texto del capcha erróneo"]},status=status.HTTP_400_BAD_REQUEST)  

        data['email']=data['username']
        serializer=self.serializer_class(data=data)
        if serializer.is_valid():
            user=serializer.save()
            managePermissions.addUserToGroup(username=data['username'], groupname='propietario')
            email_confirm_token = tokens.AccountActivationTokenGenerator().make_token(user)

            #stores the rest of the user data un core.app_user
            d={}
            d['user']=user.id
            d['data_acceptation']=data['data_acceptation']
            d['notification_acceptation']=data['notification_acceptation']
            d['interest']=data['interest']
            d['email_confirm_token']=email_confirm_token
            d['email_confirmed']=False
            
            appUserSerializer=serializers.AppUserSerializer(data=d)
            if appUserSerializer.is_valid():
                appUser=appUserSerializer.save()
            else:
                return Response(appUserSerializer.errors, status=400)
            
            #print('account_activation_token', email_confirm_token)
            emails.emailNewUserEmailConfirm(user.id, user.username, email_confirm_token)
            print('email enviado')

            if generalModule.getSetting('enviar_email_cuando_un_usuario_se_registre').lower()=="true":
                recipients = generalModule.getAllUserEmailsInGroup('receptor_email_nuevos_usuarios')
                emails.alertUserJustregistered(user.id,user.username,recipients)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class AppUserViewSet(viewsets.ModelViewSet):
    queryset = models.AppUser.objects.all()
    serializer_class = serializers.AppUserSerializer
    permission_classes = (generalAccessPolicy.AllowOnlyModifyAndListToAdmin,)



#@method_decorator(csrf_exempt, name='dispatch')
@api_view(http_method_names=['GET'])
@permission_classes((permissions.AllowAny,))
def createCaptcha(request):
    r=captchaModule.createCaptchaFunction(request)
    return JsonResponse(r)

@api_view(http_method_names=['GET'])
@permission_classes((permissions.AllowAny,))
def emailConfirmToken(request):
    """
    Sets the email as confirmed in the core.app_user table
    """
    
    pg=generalModule.getDjangoPg()
    user_id=request.GET['id']
    email_confirm_token= request.GET["email_confirm_token"]
    whereClause=WhereClause('user_id =%s and email_confirm_token=%s',[user_id, email_confirm_token])
    result=pg.pgSelect(table_name="core.app_user", string_fields_to_select="email_confirm_token,email_confirmed",whereClause=whereClause)
    if len(result) != 1:       
        t=get_template(template_name='emailUserConfirm_wrong_token.html')
        return HttpResponse(t.render({'TEMPLATE_ASSETS_URL': settings.TEMPLATE_ASSETS_URL, 'WEB_URL':settings.WEB_URL}))
    else:
        if result[0]['email_confirmed']:
            #el email ya había sido confirmado
            t=get_template(template_name='emailUserAlreadyConfirmed.html')
            return HttpResponse(t.render({'TEMPLATE_ASSETS_URL': settings.TEMPLATE_ASSETS_URL, 'WEB_URL':settings.WEB_URL}))         
        
        fieldsAndValues=FieldsAndValues({'email_confirmed':True})
        whereClause=WhereClause('user_id =%s and email_confirm_token=%s',[user_id, email_confirm_token])
        pg.pgUpdate(table_name='core.app_user', fieldsAndValues=fieldsAndValues, whereClause=whereClause)
        #pg.pgUpdate(table_name='core.app_user', oStrFielsAndValues=o, cond_where='user_id=%s', list_values_cond_where=[user_id])
        t=get_template(template_name='emailUserConfirm.html')            

        u=User.objects.get(id=user_id)
        if generalModule.getSetting('auto_activar_usuario_cuando_confirme_email')=="True":
            u.is_active=True
            u.save()
            print('usuario activado')
            mensaje=f'Su cuenta ya está activada. Puede iniciar sesión en {settings.WEB_URL}.'
        else:
            mensaje=f'Ahora debe esperar a que un miembro del equipo active su cuenta en {settings.WEB_URL}.'

        if generalModule.getSetting('enviar_email_cuando_un_usuario_confirma_su_email')=="True":
            recipients = generalModule.getAllUserEmailsInGroup('receptor_email_usuario_confirma_email')
            print(recipients)
            emails.alertUserConfirmedEmail(user_id,u.username,recipients)

        return HttpResponse(t.render({'TEMPLATE_ASSETS_URL': settings.TEMPLATE_ASSETS_URL, 'MENSAJE':mensaje}))




