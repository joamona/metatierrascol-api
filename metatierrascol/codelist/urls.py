from django.urls import path, include
from rest_framework import routers

from . import views
# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'snr_persona_titular_tipo', views.SnrPersonaTitularTipoViewSet, 'snr_persona_titular_tipo')
router.register(r'departamento', views.DepartamentoViewSet, 'departamento')
router.register(r'codelist/provincia',views.ProvinciaViewSet, 'provincia')
router.register(r'municipio',views.MunicipioViewSet, 'municipio')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
]
