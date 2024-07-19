from django.urls import path, include
from rest_framework import routers
from . import views

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'mobile_app_version',views.MobileAppVersionViewSet,'mobile_app_version')
router.register(r'mobile_app_version_notes',views.MobileAppVersionNotesViewSet,'mobile_app_version_notes')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('mobile_app_version/download_version/<version>/',views.MobileAppVersionViewSet.as_view({'get': 'download_version'}), name='download_version'),    
    path('mobile_app_version/publicar_version/<version_id>/',views.MobileAppVersionViewSet.as_view({'post': 'publicar_version'}), name='publicar_version'),    
    path('mobile_app_version/despublicar_version/<version_id>/',views.MobileAppVersionViewSet.as_view({'post': 'despublicar_version'}), name='despublicar_version'),    
    path('mobile_app_version_notes/get_version_notes/<version_id>/',views.MobileAppVersionNotesViewSet.as_view({'get': 'get_version_notes'}), name='get_version_notes'),    
]
