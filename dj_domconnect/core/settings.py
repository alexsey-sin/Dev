# -*- encoding: utf-8 -*-
import os
from datetime import timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'p&l%385148kslhtyn^##a1)ilz@4zqj=rq&agdol^##zgl9(vs'

DEBUG = True

# ALLOWED_HOSTS = ['django.domconnect.ru', '37.46.128.40', 'dj_domconnect.ru']
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrap_modal_forms',
    'rest_framework',
    # 'rest_framework_simplejwt',
    'rest_framework.authtoken',
    'app',
    'api',
    'demo',
    'mobile',
    'domconnect',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'
LOGIN_REDIRECT_URL = 'app:home'
LOGOUT_REDIRECT_URL = 'app:home'
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates/")

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
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

WSGI_APPLICATION = 'core.wsgi.application'

#############################################################
# для сервера
# DATABASES = {
#     'default': {
        # 'ENGINE': 'django.db.backends.postgresql',
        # 'NAME': 'django',
        # 'USER': 'alex',
        # 'PASSWORD': 'J3UHx4rwWR',
        # 'HOST': '127.0.0.1',
        # 'PORT': '5432',
#     }
# }

# для локального компьютера
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME'  : 'db.sqlite3',
    }
}
#############################################################

# AUTH_USER_MODEL = 'app.User'
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


LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

# USE_TZ = True
USE_TZ = False

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # 'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        # 'rest_framework.authentication.BasicAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
    ],
}
SIMPLE_JWT = {
   # Устанавливаем срок жизни токена
   'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
   'AUTH_HEADER_TYPES': ('Bearer',),
}
#############################################################
STATIC_URL = '/static/'

# для сервера
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# # для локального компьютера
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
#############################################################
MEDIA_URL = '/media/'

# для сервера
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# для локального компьютера
MEDIAFILES_DIRS = (
    os.path.join(BASE_DIR, 'media'),
)

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': True,
#     'handlers': {
#         'file': {
#             'level': 'INFO',
#             'class': 'logging.FileHandler',
#             'filename': 'main.log',
#         },
#     },
#     'loggers': {
#         'django_log': {
#             'handlers': ['file'],
#             'level': 'INFO',
#             'propagate': True,
#         },
#     },
# }

#############################################################
#############################################################
