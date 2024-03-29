from django.contrib.auth import authenticate
from . import models
from rest_framework import serializers

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
        print(user)
        if not user:
            raise serializers.ValidationError("Usuario o contraseña erróneos.")

        attrs['user'] = user
        return attrs
    

class UsuariosAvisadosDescargaZipSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UsuariosAvisadosDescargaZip
        fields = '__all__'
