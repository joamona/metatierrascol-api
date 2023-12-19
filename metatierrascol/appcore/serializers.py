from django.contrib.auth.models import User
from . import models
from rest_framework import serializers

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']

class AppSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AppSettings
        fields = '__all__'
