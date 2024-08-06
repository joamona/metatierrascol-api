# Create your views here.
#Django imports
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.contrib.auth import login
from django.contrib.auth.models import User, Group
from django.template.loader import get_template


#rest framework imports
from rest_framework import viewsets, permissions, generics, mixins
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
from .accesspolicy import generalAccessPolicy, coreViewsAcessPolicy
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


#Añade usuarios a auth_user, y a core.app_user
class DjangoAndAppUserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.DjangoUserSerializer
    permission_classes = (coreViewsAcessPolicy.DjangoAndAppUserViewsAccessPolicy,)

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
            user=serializer.save()#guarda el usuario en la tabla auth_user
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
                appUser=appUserSerializer.save() #guarda el usuario en core.app_user
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

    @action(detail=False, methods=['post'])
    def get_users(self, request, *args, **kwargs):

        username=request.data.get('username','')
        is_active=request.data.get('is_active','')
        is_superuser=request.data.get('is_superuser','')
        email_confirmed=request.data.get('email_confirmed','')
        #after_date_joined=request.data.get('after_date_joined','')
        #before_date_joined=request.data.get('before_date_joined','')
        print (request.data)

        #print('username',username)
        #print('is_active',is_active)
        #print('is_superuser',is_superuser)
        #print('after_date_joined',after_date_joined)
        #print('before_date_joined',before_date_joined)

        where='auth_user.id=app_user.user_id'
        valuesCondWhere=[]
        if username != '':
            where = where + ' and auth_user.username like %s'
            username2 = f'%{username}%'
            valuesCondWhere=[username2]

        if is_active != '':
            where = where + ' and auth_user.is_active = %s'
            if is_active == 'true' or is_active == 'True' or is_active == True:
                valuesCondWhere.append(True)
            elif is_active == 'false' or is_active == 'False' or is_active == False:
                valuesCondWhere.append(False)

        if email_confirmed != '':
            where = where + ' and app_user.email_confirmed = %s'
            if email_confirmed == 'true' or is_active == 'True' or is_active == True:
                valuesCondWhere.append(True)
            elif email_confirmed == 'false' or is_active == 'False' or is_active == False:
                valuesCondWhere.append(False)

        if is_superuser != '':
            where = where + ' and auth_user.is_superuser = %s'
            if is_superuser == 'true' or is_superuser == 'True' or is_superuser == True:
                valuesCondWhere.append(True)
            elif is_superuser == 'false' or is_superuser == 'False' or is_superuser == False:
                valuesCondWhere.append(False)

        #print(where)
        #print(valuesCondWhere) 
        pgo=generalModule.getDjangoPg()
        whereClause=WhereClause(where,valuesCondWhere)
        user_fields=pgo.pgGetTableFieldNames(table_name='public.auth_user',
            list_fields_to_remove=['id','password','first_name', 'last_name'],
            returnAsString=True)
        app_user_fields = pgo.pgGetTableFieldNames(table_name='core.app_user',
            list_fields_to_remove=['id','email_confirm_token'],
            returnAsString=True)
        app_user_fields = app_user_fields + ',app_user.id as app_user_id' 
        select_fieldnames = user_fields + ',' + app_user_fields
        limit = int(generalModule.getSetting('numero_maximo_de_filas_recuperadas'))
        r=pgo.pgSelect(table_name='public.auth_user as auth_user ,core.app_user as app_user',
                       string_fields_to_select=select_fieldnames,
                       whereClause=whereClause,limit=limit, orderBy='user_id desc')
        r2=[]
        for u in r:
            user_groups = generalModule.getUserGroups_fromUsername(u['username'])
            u['user_groups']=user_groups
            r2.append(u)
        n=len(r2)
        return Response({'message':f'Usuarios recuperados: {n}','data':r2})

    @action(detail=False, methods=['post'])
    def get_users_of_group(self, request, *args, **kwargs):
        groupId = request.data.get('groupId','')
        if groupId=='':
            return Response({'message':'Ningún grupo especificado'})
        where='auth_user.id=app_user.user_id and auth_user_groups.user_id=auth_user.id and auth_user_groups.group_id = %s'

        whereClause=WhereClause(where,[groupId])
        pgo=generalModule.getDjangoPg()
        user_fields=pgo.pgGetTableFieldNames(table_name='public.auth_user',
            list_fields_to_remove=['id','password','first_name', 'last_name'],
            returnAsString=True)
        app_user_fields = pgo.pgGetTableFieldNames(table_name='core.app_user',
            list_fields_to_remove=['id','user_id','email_confirm_token'],
            returnAsString=True)
        app_user_fields = app_user_fields + ', app_user.user_id as user_id'
        app_user_fields = app_user_fields + ',app_user.id as app_user_id' 
        select_fieldnames = user_fields + ',' + app_user_fields
        print(select_fieldnames)
        limit = int(generalModule.getSetting('numero_maximo_de_filas_recuperadas'))

        r=pgo.pgSelect(table_name='public.auth_user as auth_user ,core.app_user as app_user, public.auth_user_groups as auth_user_groups',
                       string_fields_to_select=select_fieldnames,
                       whereClause=whereClause,limit=limit, orderBy='user_id desc')

        r2=[]
        for u in r:
            user_groups = generalModule.getUserGroups_fromUsername(u['username'])
            u['user_groups']=user_groups
            r2.append(u)
        n=len(r2)
        return Response({'message':f'Usuarios recuperados: {n}','data':r2})


class DjangoUserStatusUpdate(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    Updates the is_active and is_superuser status in the table public.auth_user.
    Receives by PATCH the fields:
    - is_active 
    - is_superuser.
    It can receive only one of the parameters.
    - url: core/django_user_status_update/{id}/
    """
    queryset = User.objects.all()
    permission_classes = (generalAccessPolicy.AllowAdminOnly,)
    serializer_class = serializers.DjangoUserStatusUpdateSerializer

    def partial_update(self, request, *args, **kwargs):
        # Lógica de actualización parcial predeterminada
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        old_active_status = instance.is_active
        new_active_status = request.data.get('is_active','')
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Llama a tu función personalizada
        if generalModule.getSetting('enviar_email_al_activar_desactivar_usuarios')=='True':
            if (new_active_status != ''):
                if new_active_status == True:
                    emails.emailUserActivationAccount(instance.username)
                else:
                    emails.emailUserDeactivationAccount(instance.username)

        return Response(serializer.data)

class DjangoUserGroupsUpdate(viewsets.GenericViewSet):
    """
    Both methods recieive a user id, in the url, and the group id by POST:
    - core/django_user_groups_update/{id}/add_user_to_group/
    - core/django_user_groups_update/{id}/remove_user_from_group/
    """
    queryset = User.objects.all()
    permission_classes = (generalAccessPolicy.AllowAdminOnly,)
    serializer_class = serializers.DjangoUserGroupsUpdateSerializer

    @action(detail=True, methods=['post'])
    def add_user_to_group(self, request, *args, **kwargs):
        ser=serializers.DjangoUserGroupsUpdateSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        groupId=ser.validated_data['groupId']
        u:User = self.get_object()
        group = Group.objects.filter(id=groupId).first()#None si no existe
        if not group:
            return Response({'error':['El id del grupo no existe']})
        u.groups.add(Group.objects.get(id=groupId))
        groupName = group.name
        return Response({'message':[f'Usuario añadido al grupo: {groupName}']})

    @action(detail=True, methods=['post'])
    def remove_user_from_group(self, request, *args, **kwargs):
        ser=serializers.DjangoUserGroupsUpdateSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        groupId=ser.validated_data['groupId']
        u:User = self.get_object()
        group = Group.objects.filter(id=groupId).first()#None si no existe
        if not group:
            return Response({'error':['El id del grupo no existe']})
        groupName = group.name
        u.groups.remove(Group.objects.get(id=groupId))
        return Response({'message':[f'Usuario eliminado del grupo: {groupName}']})

#Para manejar solo la tabla core.app_user
class AppUserViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    Manages the table core.app_user
    """
    queryset = models.AppUser.objects.all()
    serializer_class = serializers.AppUserSerializer
    permission_classes = (generalAccessPolicy.AllowOnlyModifyAndListToAdmin,)
    
    
    def partial_update(self, request, *args, **kwargs):
                # Llama al método original para realizar la actualización parcial
        response = super().partial_update(request, *args, **kwargs)
        
        # Accede a la instancia actualizada
        instance = self.get_object()

        # Serializa los campos personalizados que deseas devolver
        custom_response_data = {
            'email_confirmed': instance.email_confirmed
        }
        
        # Retorna la respuesta personalizada
        return Response(custom_response_data, status=status.HTTP_200_OK)

@api_view(http_method_names=['GET'])
@permission_classes((permissions.AllowAny,))
def createCaptcha(request):
    r=captchaModule.createCaptchaFunction(request)
    return JsonResponse(r)

@api_view(http_method_names=['GET'])
@permission_classes((permissions.AllowAny,))
def emailConfirmToken(request):
    """
    Sets the email as confirmed in the core.app_user table.
    Responds with a template:
    - Wrong token
    - Email already confirmed
    - Email confirmed
    """
    
    pg=generalModule.getDjangoPg()
    user_id=request.GET['id']
    email_confirm_token= request.GET["email_confirm_token"]
    whereClause=WhereClause('user_id =%s and email_confirm_token=%s',[user_id, email_confirm_token])
    result=pg.pgSelect(table_name="core.app_user", string_fields_to_select="email_confirm_token,email_confirmed",whereClause=whereClause)
    if len(result) != 1:       
        t=get_template(template_name='confirm_email/emailUserConfirm_wrong_token.html')
        return HttpResponse(t.render({'TEMPLATE_ASSETS_URL': settings.TEMPLATE_ASSETS_URL, 'WEB_URL':settings.WEB_URL}))
    else:
        if result[0]['email_confirmed']:
            #el email ya había sido confirmado
            t=get_template(template_name='confirm_email/emailUserAlreadyConfirmed.html')
            return HttpResponse(t.render({'TEMPLATE_ASSETS_URL': settings.TEMPLATE_ASSETS_URL, 'WEB_URL':settings.WEB_URL}))         
        
        fieldsAndValues=FieldsAndValues({'email_confirmed':True})
        whereClause=WhereClause('user_id =%s and email_confirm_token=%s',[user_id, email_confirm_token])
        pg.pgUpdate(table_name='core.app_user', fieldsAndValues=fieldsAndValues, whereClause=whereClause)
        #pg.pgUpdate(table_name='core.app_user', oStrFielsAndValues=o, cond_where='user_id=%s', list_values_cond_where=[user_id])
        t=get_template(template_name='confirm_email/emailUserConfirm.html')            

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

#gestión de grupos
class DjangoGroupsViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all().order_by('id')
    serializer_class = serializers.DjangoGroupSerializer
    permission_classes = (coreViewsAcessPolicy.DjangoGroupsViewsAccessPolicy,)


class AppSettingsViewSet(viewsets.ModelViewSet):
    queryset = models.AppSettings.objects.all().order_by('id')
    serializer_class = serializers.AppSettingsSerializer
    permission_classes = (coreViewsAcessPolicy.AppSettingsViewsAccessPolicy,)
    
    @action(detail=False, methods=['post'])
    def get_parameter_value_by_name(self, request, *args, **kwargs):
        parameter_name = request.data.get('parameter_name')
        parameter_value = generalModule.getSetting(parameter_name)
        return Response({'message':'Parámetro recuperado con éxito', 'parameter_name':parameter_name, 'parameter_value': parameter_value})

class AppSettingsList(viewsets.ModelViewSet):
    """
    Not usefull. Created for testing
    """
    queryset = models.AppSettings.objects.all()#el queriset trabaja con todos los obj
						#es una variable de clase
    serializer_class = serializers.AppSettingsSerializer #es una variable de clase
    permission_classes = (generalAccessPolicy.AllowAuthenticatedSafeMethods,)#esto permite 
        #a todos los métodos ser usados, 
        #pero cada método puede tener unos permisos diferentes con el siguiente decorador:
        # @action(detail=True, methods=['post'], permission_classes=[IsAdminOrIsSelf])
        #       detail=True significa que trabaje con varios registros
    def retrieve(self, request, id=None):#fíjate que recibe request y un parámetro de la url
        #print(self.basename, self.action, self.detail, self.suffix, self.name, self.description)
        qs2=self.queryset.filter(id__lt=id)#cojo el queryset de la variable de clase y le aplico
			#el filtro gid < the_gid. → lt significa less than
        s = self.get_serializer(qs2, many=True)#obtiene el serializer de la clase
			#many significa que puede trabajar
			#con varios registros, no solo uno
        return Response(s.data)
    