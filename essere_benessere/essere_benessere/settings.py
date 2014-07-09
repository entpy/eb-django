"""
Django settings for essere_benessere project.

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
SECRET_KEY = 'yip_19%5hfjm+vjwq=^zl48sf%cqrtmc7a#x8#+775mcticg!c'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'website',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'essere_benessere.urls'

WSGI_APPLICATION = 'essere_benessere.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

# postgreSQL
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'eb_website',
        'USER': 'testuser',
        'PASSWORD': 'testuser',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

"""
# MySQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'eb_website',
        'USER': 'testuser',
        'PASSWORD': 'testuser',
        'HOST': '127.0.0.1',
        'PORT': '3306',
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

# inside app
STATIC_URL = '/static/'

MEDIA_ROOT = '/tmp/'
MEDIA_URL = '/tmp/'
ADMIN_MEDIA_PREFIX = '/media/admin/'

#inside project
STATICFILES_DIRS = (
	os.path.join(BASE_DIR, "static"), #inside project
)

"""
HOW TO SUL LOGGING
------------------

Il logger e' un contenitore per i log, vengono inseriti dentro di esso
solo se i livelli di logging del file sono >= a quelli del contenitore

l' handler del logger gestisce dove i messaggi di log raccolti dal logger
andranno spediti, per esempio su file, console, ecc..

E' inoltre possibile impostare filtri e formattazione per i log
(per ora qui non viene fatto!)
"""
LOGGING = {
	'version': 1,
	'disable_existing_loggers': False,
	'handlers': {
		'file': {
			'level': 'DEBUG',
			'class': 'logging.FileHandler',
			'filename': '/tmp/debug.log',
		},
		'console' : {
			'class' : 'logging.StreamHandler',
			'level' : 'INFO',
			'stream' : 'ext://sys.stdout',
		},
	},
	'loggers': {
		'django.request': {
			'handlers': ['file'],
			'level': 'DEBUG',
			'propagate': True,
		},
	},
}
