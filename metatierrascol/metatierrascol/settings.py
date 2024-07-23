"""
Django settings for metatierrascol project.

Generated by 'django-admin startproject' using Django 4.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path
from datetime import timedelta

FORCE_SCRIPT_NAME=os.getenv('FORCE_SCRIPT_NAME')

API_URL=os.getenv('API_URL')#El dominio y alias de acceso a la API, con BARRA FINAL. 
                            #Ej https://mydomain.com/metatierrascol-api/
WEB_URL=os.getenv('WEB_URL')#La dirección a la web. Se usa en los emails
TEMPLATE_ASSETS_URL=os.getenv('TEMPLATE_ASSETS_URL')#dirección de los archivos
                                    #estáticos usados en las plantillas

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = 'django-insecure-+z_6n94l($5goa6gopn&ugrsy#+g8i@w3zctzt+knb%&&l)z2v'
SECRET_KEY=os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", 'False').lower() in ('true', '1', 't')

ALLOWED_HOSTS = [os.getenv('DJANGO_ALLOWED_HOSTS')]
CSRF_TRUSTED_ORIGINS=['https://metatierrascol.upvusig.car.upv.es']

#DJANGO_SEND_EMAIL_ON_FILE_UPLOAD=os.getenv('DJANGO_SEND_EMAIL_ON_FILE_UPLOAD','True').lower() in ('true', '1', 't')
FILE_UPLOAD_MAX_MEMORY_SIZE = float(os.getenv('DJANGO_FILE_UPLOAD_MAX_MEMORY_SIZE','204857600'))
# Application definition

#For password reset site configuration
#USE_X_FORWARDED_HOST=os.getenv('SECURE_PROXY_SSL_HEADER', 'False').lower() in ('true',1,'t')
#SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', os.getenv('SECURE_PROXY_SSL_HEADER'))

SITE_ID=2

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'captcha',
    'drf_yasg',
    'rest_framework',
    'knox',
    'django_filters',
    'corsheaders',
    'codelist',#listas codificadas
    'core',#configuraciones, autenticación, utilidades generales
    'party',#usuarios
    'rrr',#derechos
    'baunit',#unidades basicas (predios)
    'spatialunit',#unidades espaciales, un predio puede tener varias versiones de unidad espacial
    'source',#manejo de documentos
    'mobileappversion'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOW_ALL_ORIGINS=True

ROOT_URLCONF = 'metatierrascol.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'core/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'metatierrascol.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('POSTGRES_HOST'),
        'PORT': os.getenv('POSTGRES_PORT'),
        'OPTIONS': {
            'options': '-c search_path=public',
        }
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = os.getenv('TIME_ZONE')

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = os.getenv('DJANGO_STATIC_URL')
MEDIA_URL = 'media/'

#STATIC_ROOT = '/usr/src/static_root'
STATIC_ROOT = BASE_DIR / 'static_root'
MEDIA_ROOT = BASE_DIR / 'media_root'


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': ('knox.auth.TokenAuthentication',),
}
REST_KNOX = {
    #'USER_SERIALIZER':'accounts.serializers.UserSerializer',
    'TOKEN_TTL': timedelta(hours=72),
    'TOKEN_LIMIT_PER_USER':10,
}

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'api_key': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    },
    #"is_authenticated": False,  # Set to True to enforce user authentication,
    "is_superuser": True,  # Set to True to enforce admin only access

}

LOGIN_URL = 'rest_framework:login'
LOGOUT_URL = 'rest_framework:logout'


EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS','True').lower() == 'true' #Devuelve True si se cumple
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_UPV = os.getenv('EMAIL_UPV')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_FROM = os.getenv('EMAIL_FROM')
ADMINS=[('Gaspar Mora', 'joamona@cgf.upv.es')]

if DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
    EMAIL_FILE_PATH = BASE_DIR / "sent_emails"

#para habilitar los signals
#os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
