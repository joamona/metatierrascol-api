
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
#from django.contrib.auth import password_validation
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from django.contrib.auth.models import User

class ResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    new_password=serializers.CharField(required=True)
    confirm_password=serializers.CharField(required=True)

    def validate_new_password(self,value):
        user = User(
            username=self.initial_data.get('email'),
            email=self.initial_data.get('email')
        )
        try:
            validate_password(value, user)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value  
    def validate_confirm_password(self,value):
        if not self.initial_data.get('new_password')==self.initial_data.get('confirm_password'):
            raise serializers.ValidationError('Las contraseñas introducidas no son iguales')
        return value