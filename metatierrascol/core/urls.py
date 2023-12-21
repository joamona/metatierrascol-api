from django.urls import path, include
from rest_framework import routers

from knox import views as knox_views

from . import views
# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'core/appsettings',views.AppSettingsViewSet, 'appsettings')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path(r'core/hello_world/', views.helloWorld, name='hello_world'),
    path(r'core/knox/login/', views.LoginViewWithKnox.as_view(), name='knox_login'),
    path(r'core/knox/logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path(r'core/knox/logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),    
    path('', include(router.urls)),
    path('core/appsettings_list/<gid>/',views.AppSettingsList.as_view({'get': 'retrieve'}), name='appsetings_list'),
    path('core/appsettings_list_query/',views.AppSettingsListQuery.as_view(), name='appsetings_list_query'),    
]
