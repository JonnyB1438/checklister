"""
Django settings for checklister project.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
from os import path
from pathlib import Path
from . import variables

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-fw5_h*j#(izn2dxmu#uwi^dv1*+m4=*ahpw7rdc_5vn-oq(ppw'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = variables.DEBUG

ALLOWED_HOSTS = ['checklister.site',
                 '127.0.0.1',
                 'localhost',
                 ]

# Application definition
INSTALLED_APPS = [
    'apps.checklist',
    'apps.users',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'social_django',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': variables.DBNAME,
        'USER': variables.DBUSERNAME,
        'PASSWORD': variables.DBPASSWORD,
        'HOST': variables.DBHOST,
        'PORT': variables.DBPORT,
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = path.join(BASE_DIR, 'static')
STATICFILES_DIR = []

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = "/auth/login/"
LOGIN_REDIRECT_URL = "checklist"
LOGOUT_REDIRECT_URL = "checklist"

SOCIAL_AUTH_JSONFIELD_ENABLED = True

SOCIAL_AUTH_VK_OAUTH2_KEY = variables.SOCIAL_AUTH_VK_OAUTH2_KEY
SOCIAL_AUTH_VK_OAUTH2_SECRET = variables.SOCIAL_AUTH_VK_OAUTH2_SECRET

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = variables.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = variables.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET

# SOCIAL_AUTH_VK_OAUTH2_SCOPE = ['email', ]
# SOCIAL_AUTH_PIPELINE = (
#     'social_core.pipeline.social_auth.social_details',
#     'social_core.pipeline.social_auth.social_uid',
#     'social_core.pipeline.social_auth.social_user',
#     'social_core.pipeline.user.get_username',
#     'social_core.pipeline.social_auth.associate_by_email',
#     'social_core.pipeline.user.create_user',
#     'social_core.pipeline.social_auth.associate_user',
#     'social_core.pipeline.social_auth.load_extra_data',
#     'social_core.pipeline.user.user_details',
# )

AUTHENTICATION_BACKENDS = (
    'social_core.backends.vk.VKOAuth2',  # vk auth
    'social_core.backends.google.GoogleOAuth2',  # google auth
    'django.contrib.auth.backends.ModelBackend',  # clasic auth
)

SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'
SOCIAL_AUTH_URL_NAMESPACE = 'social'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
EMAIL_HOST_USER = variables.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = variables.EMAIL_HOST_PASSWORD
DEFAULT_FROM_EMAIL = variables.DEFAULT_FROM_EMAIL

SERVER_EMAIL = EMAIL_HOST_USER
