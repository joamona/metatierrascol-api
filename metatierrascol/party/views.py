# Create your views here.
#Django imports
from django.http import JsonResponse, HttpRequest
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.shortcuts import get_object_or_404

#rest framework imports
from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
from django_filters import rest_framework as filters
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView

from knox.auth import TokenAuthentication
from knox.views import LoginView as KnoxLoginView

#mis módulos
from . import serializers

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer