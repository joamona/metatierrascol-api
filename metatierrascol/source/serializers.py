from rest_framework import serializers
from .models import ArchivoZip

class ArchivoZipSerializer(serializers.ModelSerializer):
    class Meta:
        model=ArchivoZip
        fields="__all__"
