from django.urls import path, include
from rest_framework import routers

from knox import views as knox_views

from . import views, resetPasswordViews
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
    path('email_confirm_token/', views.emailConfirmToken,name='email_confirm_token'),

    path ('request_reset_password_email/',resetPasswordViews.RequestResetPasswordEmail.as_view(),name='request_reset_password_email'),
    path('send_reset_password_form/<token>/', resetPasswordViews.sendResetPasswordForm, name='send_reset_password_form'),
    path('perform_reset_password/<token>/', resetPasswordViews.PerformResetPassword.as_view(),name='perform_reset_password')
]
#Explicación proceso reset password
    #path ('request_reset_password_email',resetPasswordViews.RequestPasswordReset.as_view(),'request_reset_password_email'),
    #genera un token y lo envía por email para que lo pinche el usuario en una url.
    #la url es send_reset_password_form/<token>/, que se describe abajo

    #path('send_reset_password_form/<token>/', resetPasswordViews.sendResetPasswordForm, name='send_reset_password_form'),
    #Con el token recibido en el email, esta vista envíe el formulario
    #para poner la contraseña dos veces

    #path('reset_password/<token>/', resetPasswordViews.ResetPassword.as_view(),name='reset_password')
    #Evalúa las contraseñas  y reestablece la contraseña.
    #el botón submit de send_reset_password_form/<token>/ 
    #envía la contraseña a esta vista
