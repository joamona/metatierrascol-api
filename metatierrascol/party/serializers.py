from enum import unique
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from . import models
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
"""

# Serializers define the API representation.
class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    read_only_fields = ['id']
    class Meta:
        model = User
        fields = ['id','email', 'password', 'is_active']
        ref_name = 'UserSerializer'

    def create(self, validated_data):
        print("Creando")
        validated_data['username']=validated_data.get('email')
        validated_data['is_active']=False
        u=User(**validated_data)
        u.set_password(validated_data['password'])
        u.save()
        return validated_data

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.content = validated_data.get('password', instance.password)
        instance.created = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance 
"""