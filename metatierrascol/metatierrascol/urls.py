"""metatierrascol URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib.auth.decorators import login_required

#from .views import CustomPasswordResetView

schema_view = get_schema_view(
   openapi.Info(
      title="MetaTierras Colombia API",
      default_version='v1',
      description="MetaTierras Colombia API",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="joamona@cgf.upv.es"),
      license=openapi.License(name="GPL License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
#    path("accounts/", include("django.contrib.auth.urls")),
#    path('admin/', admin.site.urls),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'), 
    path('swagger/', login_required(schema_view.with_ui('swagger', cache_timeout=0)), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('core/', include('core.urls')),
    path('codelist/', include('codelist.urls')),
    path('party/', include('party.urls')),
    path('baunit/', include('baunit.urls')),    
    path('source/', include('source.urls')),    
    path('mobileappversion/', include('mobileappversion.urls')),   
    path('captcha/', include('captcha.urls')), 

]
#django.contrib.auth.urls includes the following urls
#accounts/login/ [name='login']
#accounts/logout/ [name='logout']
#accounts/password_change/ [name='password_change']
#accounts/password_change/done/ [name='password_change_done']
#accounts/password_reset/ [name='password_reset']
#accounts/password_reset/done/ [name='password_reset_done']
#accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
#accounts/reset/done/ [name='password_reset_complete']


#A JSON view of your API specification at /swagger.json
#A YAML view of your API specification at /swagger.yaml
#A swagger-ui view of your API specification at /swagger/
#A ReDoc view of your API specification at /redoc/
