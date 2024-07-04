from django.urls import path, include
from rest_framework import routers

from . import views
# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'archivo_zip',views.ArchivoZip, 'archivo_zip')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('descarga_zip_codigo_acceso/<codigo_acceso>/',views.DescargaArchivoZipCodigoAcceso.as_view(), name='descarga_zip_codigo_acceso'),
#    path('añade_fichero_zip/',views.AñadeFicheroZip.as_view()),
]
