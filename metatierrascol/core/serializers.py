from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from rest_framework import serializers
from django.contrib.auth.models import User

from . import models

class AppSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AppSettings
        fields = '__all__'

    def validate(self, attrs):
        validated = super().validate(attrs)
        print ("Validando")
        print(validated)
        #poner aquí las condiciones
        #para sacar los valores se pone
        #attrs.get('atributo')
        #si los valores son correctos, devuelve return attrs
        #si hay error return serializers.ValidationError('El mensaje')
        return validated


class LoginViewWithKnoxSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)

    def validate_username(self,value):
        #validate_propiedad permite hacer validaciones adicionales sobre los campos
        #if len(value) > 10:
        #    raise serializers.ValidationError('Username mayor que 10')
        return value#hay que devolver un valor
    
    def validate(self, attrs): #se ejecuta con serializer.is_valid(raise_exception=True)
                    #e inicializa validated_data, con los datos validados, que es un dict
        username = attrs.get('username')
        password = attrs.get('password')
        user = authenticate(request=self.context.get('request'), username=username,
                            password=password)
        #print(user)
        if not user:
            raise serializers.ValidationError("Usuario o contraseña erróneos.")

        attrs['user'] = user
        return attrs
    

class UsuariosAvisadosDescargaZipSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UsuariosAvisadosDescargaZip
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email','is_superuser','is_active', 'password']
        ref_name = 'UserSerializer'
    def validate_email(self,value):
        email = value
        if len(email) < 4:
            raise serializers.ValidationError('El email debe tener más de 4 caracteres')
        if not '@' in email:
            raise serializers.ValidationError('El email debe tener un carácter @')
        if not '.' in email:
            raise serializers.ValidationError('El email debe tener un carácter .')
        return value
    
    def validate_password(self, value):
        user = User(
            username=self.initial_data.get('username'),
            email=self.initial_data.get('email')
        )
        try:
            validate_password(value, user)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value        

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.is_active=False
        user.save()
        return user
    
class AppUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AppUser
        fields = ['id','user', 'data_acceptation', 'notification_acceptation', 'interest',
                    'email_confirm_token', 'email_confirmed']   
