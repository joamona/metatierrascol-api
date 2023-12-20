from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from . import models
from rest_framework import serializers

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

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


class LoginViewWithKnoxSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        username = attrs.get('username').lower()
        password = attrs.get('password')

        user = authenticate(request=self.context.get('request'), username=username,
                            password=password)
        if not user:
            raise serializers.ValidationError("Usuario o contraseña erróneos.")

        attrs['user'] = user
        return attrs