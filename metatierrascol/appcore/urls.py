from django.urls import path, include
from rest_framework import routers

from appcore import views
# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'core/users', views.UserViewSet, 'users')
router.register(r'core/appsettings',views.AppSettingsViewSet, 'appsettings')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('appsettings_list/<gid>/',views.AppSettingsList.as_view({'get': 'retrieve'}), name='appsetings_list'),
]
