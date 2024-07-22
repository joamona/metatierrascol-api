from django.urls import path, include
from rest_framework import routers

from knox import views as knox_views

from . import views
# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'appsettings',views.AppSettingsViewSet, 'appsettings')
#router.register(r'usuarios_avisados_descarga_zip',views.UsuariosAvisadosDescargaZipViewSet, 'usuarios_avisados_descarga_zip')
router.register(r'user',views.UserViewSet,'user')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('hello_world/', views.helloWorld, name='hello_world'),
    path('knox/is_valid_token/', views.isValidToken, name='is_valid_token'),
    path('knox/login/', views.LoginViewWithKnox.as_view(), name='knox_login'),
    path('knox/logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('knox/logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),    
    path('', include(router.urls)),
    path('appsettings_list/<id>/',views.AppSettingsList.as_view({'get': 'retrieve'}), name='appsetings_list'),
    path('appsettings_list_query/',views.AppSettingsListQuery.as_view(), name='appsetings_list_query'), 
    path('create_captcha/', views.createCaptcha,name='create_captcha'),
    path('email_confirm_token/', views.emailConfirmToken,name='email_confirm_token')
]
