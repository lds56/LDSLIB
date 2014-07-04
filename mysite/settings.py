"""
Django settings for mysite project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'k%&2l4(6m==y2%55!53c7h2k)be=-*bjmsl&*l*ip=7t5&%u)l'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

TEMPLATE_DIRS = (
    '/home/rui/mysite/templates',
    #os.path.join(os.path.dirname(__file__), 'templates').replace('\\','/'),
)

# Application definition

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.messages.context_processors.messages',
    'django.contrib.auth.context_processors.auth'
)	

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'library',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'mysite.urls'

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
	# 'default': {  
       #'ENGINE': 'django.db.backends.sqlite3',
       #'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
   'default': {
	'ENGINE': 'mysql.connector.django',
	'NAME': 'test',
	'USER': 'root',
	'PASSWORD': '19941018',
	'HOST': '',
	'PORT': '',
        'OPTIONS': {
          'autocommit': True,
        },
   }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
#STATIC_ROOT = '/home/rui/code/env1/local/lib/python2.7/site-packages/django/contrib/admin/static/'
STATIC_ROOT = '/home/rui/mysite/static/home/'
#STATIC_ROOT = os.path.join(os.path.dirname(__file__), '../static')
STATICFILES_DIRS = (
    #'/home/rui/static/js/',
    #'/home/rui/static/css/',
    #'/home/rui/static/images/',
    #'/home/rui/mysite/static/home/',
    #("css", os.path.join(STATIC_ROOT,'css')),
    #("js", os.path.join(STATIC_ROOT,'js')),
    #("images", os.path.join(STATIC_ROOT,'images')),
    '/home/rui/admin/',
    '/home/rui/home/',
)
