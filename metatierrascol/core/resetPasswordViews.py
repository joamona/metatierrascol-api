from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from rest_framework import status
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework import permissions
from django.http import HttpResponse
from django.template.loader import get_template

from .models import PasswordReset
from metatierrascol.settings import API_URL, TEMPLATE_ASSETS_URL
from .commonlibs import emails
from .resetPasswordSerializers import ResetPasswordRequestSerializer, ResetPasswordSerializer


class RequestPasswordReset(generics.GenericAPIView):
    """
    Sends an email with a link to see a form to put the new password
    """
    permission_classes = [AllowAny]
    serializer_class = ResetPasswordRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        email = request.data['email']
        user = User.objects.filter(email__iexact=email).first()

        if user:
            if PasswordReset.objects.filter(email=email).exists():
                return Response({'success': ['Ya le enviamos un email para reestablecer la contraseña. Busque el email.']}, status=status.HTTP_200_OK)
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user) 
            reset = PasswordReset(email=email, token=token)
            reset.save()

            reset_url = API_URL + f'core/send_reset_password_form/{token}/'
            emails.checkEmailToken(email,reset_url)

            return Response({'success': ['Le hemos enviado un email para reestablecer la contraseña']}, status=status.HTTP_200_OK)
        else:
            return Response({'success': ['Le hemos enviado un email para reestablecer la contraseña2']}, status=status.HTTP_200_OK)

class PerformResetPassword(generics.GenericAPIView):
    """
    Receives the token, and the new password twice:
        - cheks the token and gets the email
        - checks the password strength
        - sets the new password
    """
    serializer_class = ResetPasswordSerializer
    permission_classes = [AllowAny]

    def post(self, request, token):
        
        #new_password = request.POST['new_password']
        #confirm_password = request.POST['confirm_password']
        
        #if new_password != confirm_password:
        #    return Response({"error": ["Las contraseñas no coinciden"]}, status=400)
        
        reset_obj = PasswordReset.objects.filter(token=token).first()
        
        if not reset_obj:
            return Response({'error':['Token inválido']}, status=400)
        
        user = User.objects.filter(email=reset_obj.email).first()
                
        if user:
            data=request.data.copy()
            data['email']=user.email
            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data
            user.set_password(data['new_password'])
            user.save()
            reset_obj.delete()
            
            return Response({'success':['Contraseña actualizada']})
        else: 
            return Response({'success':['Contraseña actualizada2']})



#@method_decorator(csrf_exempt, name='dispatch')
@api_view(http_method_names=['GET'])
@permission_classes((permissions.AllowAny,))
def sendResetPasswordForm(request, token):
    t=get_template(template_name='passwordreset/custom_password_reset_form.html')
    endpoint_url = API_URL + f'core/reset_password/{token}/'
    return HttpResponse(t.render({'token': token, 'endpoint_url': endpoint_url, 'TEMPLATE_ASSETS_URL':TEMPLATE_ASSETS_URL}))
