"""
Django settings for novells_site project.

Generated by 'django-admin startproject' using Django 3.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '3uby7wv_r$o0gyvt1wmx+j9rv!xuc@l%0r45!+68%nu5=8$+wd'

# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = False
DEBUG = True

if DEBUG:
    ALLOWED_HOSTS = ['*']
else:
    ALLOWED_HOSTS = ['31.31.203.141', 'privereda1.ru', 'oksiji13.ru', 'www.oksiji13.ru','www.privereda1.ru','127.0.0.1']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'core.apps.CoreConfig',
    'allauth',
    'allauth.account',
    'tinymce',
    'online_users',
    'rest_framework',
    'smart_selects',
    'sorl.thumbnail',
    'colorfield',

    # 'allauth.socialaccount',

]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'online_users.middleware.OnlineNowMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    #'core.middleware.MultiSiteMiddleware',
]

ROOT_URLCONF = 'novells_site.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'novells_site.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases


if 1==0: #DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
            'OPTIONS': {
                'timeout': 30
            }
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'novells_database',
            'USER': 'novells_database_user',
            'PASSWORD': 'nnpassword',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

USE_DJANGO_JQUERY = True

LOGIN_REDIRECT_URL = '/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

if DEBUG:
    STATIC_URL = '/static/'
    STATIC_DIR = os.path.join(BASE_DIR, 'static')
    STATICFILES_DIRS = [STATIC_DIR]
    # STATIC_ROOT = os.path.join(BASE_DIR, 'static')
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
else:
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
    MEDIA_ROOT = '/root/site/media'
    STATIC_URL = '/static/'
    MEDIA_URL = '/media/'

if DEBUG:
    # EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    ACCOUNT_EMAIL_REQUIRED = True
    ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1
    ACCOUNT_EMAIL_VERIFICATION = False
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    ACCOUNT_EMAIL_REQUIRED = True
    ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1
    ACCOUNT_EMAIL_VERIFICATION = True
    # ACCOUNT_USERNAME_MIN_LENGTH = 1

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
# EMAIL_HOST_USER = 'privereda1bl@gmail.com'
# EMAIL_HOST_PASSWORD = '7rW4QObVsh'
EMAIL_HOST_USER = 'privereda1blnovell@gmail.com'
EMAIL_HOST_PASSWORD = '{c{IaqaeZMKKY|x7'

TINYMCE_DEFAULT_CONFIG = {
    "height": "500px",
    "width": "80%",
    "menubar": "file edit view insert format tools table help",
    "plugins": "advlist autolink lists link image charmap print preview anchor searchreplace visualblocks code "
               "fullscreen insertdatetime media table paste code help wordcount spellchecker",
    "toolbar": "undo redo | bold italic underline strikethrough | fontselect fontsizeselect formatselect | alignleft "
               "aligncenter alignright alignjustify | outdent indent |  numlist bullist checklist | forecolor "
               "backcolor casechange permanentpen formatpainter removeformat | pagebreak | charmap emoticons | "
               "fullscreen  preview save print | insertfile image media pageembed template link anchor codesample | "
               "a11ycheck ltr rtl | showcomments addcomment code",
    "custom_undo_redo_levels": 10,

}
