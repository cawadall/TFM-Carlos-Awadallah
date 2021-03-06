# -*- coding: utf-8 -*-

"""
Generated by 'django-admin startproject' using Django 1.11.
"""

import os
from github import Github

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ------------------------------------- DIRECTORIOS -------------------------------------------

# Exercises Directory
EXERCISES_DIR = os.path.join(BASE_DIR, 'exercises')

# Users Local Directory
USERS_LOCAL_DIR = os.path.join(BASE_DIR, 'users')

# Drivers Directory
DRIVERS_DIR = os.path.join(BASE_DIR, 'drivers')


# GitHub Users Directroy
GITHUB_USERS_DIR = '/users/'

# ------------------------------------- DIRECTORIOS -------------------------------------------


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'c$a+p1i=zzj9*vl$=78o9wr#x^k@xyzhm+d@#w1am457*26jkn'

#GITHUB_WEBHOOK_KEY ="PYZUuCetkX3PCDqQid1aMO127r5g57F9TqkbcNPJLsYTVEtLL6"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

ADMINS = (('Carlos Awadallah', 'carlosawadallah@gmail.com'))
# Extended user model
AUTH_USER_MODEL = 'local_execution_app.User'

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'local_execution_app',
    'django_extensions',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tfm_webserver.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [EXERCISES_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n', # Internacionalization
            ],
        },
    },
]

WSGI_APPLICATION = 'tfm_webserver.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': "tfmbbdd",
        'USER': "tfm",
        'PASSWORD': "masterrobotica",
        'HOST' : "localhost",
        'PORT': "3306",
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/
LANGUAGE_CODE = 'en-En' #'es-Es'

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

from django.utils.translation import ugettext_lazy as _
LANGUAGES = (
    ('es', _('Spanish')), #('es-es', _('Spanish')),
    ('en', _('English')), #('en-us', _('English')),
)


TIME_ZONE = 'Europe/Madrid'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
    EXERCISES_DIR,
]

# Media root es usado para subir archivos.
MEDIA_ROOT = os.path.join(BASE_DIR, 'users')


if DEBUG:
    DOCKER_SIMULATION_IMAGE = 'unibotics/simulation:sin-tls'
else: 
    DOCKER_SIMULATION_IMAGE = 'unibotics/simulation:latest'



# ------------------------------- GITHUB API ---------------------------------------------------------

GITHUB_REPOSITORY = "TFM-Carlos-Awadallah"

GITHUB_TOKEN = Github('d3d45f1b5818bb07526dc60d3ff9e95e598b0e42')
GITHUB_USER = GITHUB_TOKEN.get_user()
REPOSITORY = GITHUB_USER.get_repo(GITHUB_REPOSITORY)


