"""
Django settings for classifiedads project.

Generated by 'django-admin startproject' using Django 5.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
from pathlib import Path
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.flatpages',
    'django.contrib.sites',
    'fpages',
    'accounts',
    'adsboard',
    'ckeditor',
    'crispy_forms',
    'django_filters',
    'django_apscheduler',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'classifiedads.urls'

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

WSGI_APPLICATION = 'classifiedads.wsgi.application'

# AUTH_USER_MODEL = 'adsboard.User'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'formatters': {
        'simple': {
            'format': '%(asctime)s %(levelname)s %(message)s'
        },
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(message)s',
        },
        'warning': {
            'format': '%(asctime)s %(levelname)s %(message)s\nPath: %(pathname)s',
        },
        'error': {
            'format': '%(asctime)s %(levelname)s %(message)s\nPath: %(pathname)s\nStack trace: %(exc_info)s',
        },
        'mail': {
            'format': '%(asctime)s %(levelname)s %(message)s\nPath: %(pathname)s',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'console_warning': {
            'level': 'WARNING',
            'filters': ['debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'warning',
        },
        'console_error': {
            'level': 'ERROR',
            'filters': ['debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'error',
        },
        'general_file': {
            'level': 'INFO',
            'filters': ['debug_false'],
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'general.log'),
            'formatter': 'verbose',
        },
        'errors_file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'errors.log'),
            'formatter': 'error',
        },
        'security_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'security.log'),
            'formatter': 'verbose',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'mail',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'console_warning', 'console_error', 'general_file', 'errors_file', 'security_file',
                         'mail_admins'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['errors_file', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.server': {
            'handlers': ['errors_file', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.template': {
            'handlers': ['errors_file'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['errors_file'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['security_file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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

ACCOUNT_EMAIL_REQUIRED = os.getenv('ACCOUNT_EMAIL_REQUIRED')
ACCOUNT_UNIQUE_EMAIL = os.getenv('ACCOUNT_UNIQUE_EMAIL')
ACCOUNT_USERNAME_REQUIRED = os.getenv('ACCOUNT_USERNAME_REQUIRED')
ACCOUNT_AUTHENTICATION_METHOD = os.getenv('ACCOUNT_AUTHENTICATION_METHOD')
ACCOUNT_EMAIL_VERIFICATION= 'mandatory'
ACCOUNT_CONFIRM_EMAIL_ON_GET = os.getenv('ACCOUNT_CONFIRM_EMAIL_ON_GET')
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 14
ACCOUNT_FORMS = {'signup': 'accounts.forms.SignupForm'}

APSCHEDULER_DATETIME_FORMAT = 'N j, Y, f:s a'
APSCHEDULER_RUN_NOW_TIMEOUT = 25

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
EMAIL_SUBJECT_PREFIX = "Classified Ads Portal"  # заменить стандартную надпись Django в фреймворках
SERVER_EMAIL = os.getenv('SERVER_EMAIL')

ADMINS = os.getenv('ADMINS'),
MANAGERS = os.getenv('MANAGERS'),

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

LANGUAGES = [
    ('en-us', 'English'),
    ('ru', 'Русский')
]

MODELTRANSLATION_TRANSLATION_FILES = (
    'django.contrib.flatpages',
)

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_TZ = True

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale')
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static'

STATICFILES_DIRS = [
    BASE_DIR / "additional/static"
]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SITE_URL = 'http://127.0.0.1:8000'

LOGIN_REDIRECT_URL = "post_list"
