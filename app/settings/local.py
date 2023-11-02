import os
import environ
from decouple import config
env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = config('SECRET_KEY')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', cast=bool)

SYSTEM_HOST = config("SYSTEM_HOST", default="localhost")

# ALLOWED_HOSTS = [SYSTEM_HOST]
# ALLOWED_HOSTS = ['127.0.0.1','localhost']
ALLOWED_HOSTS = []

# os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.gis',
    'django.contrib.sites',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    # personal apps
    'authentication',
    'blog',
    'analytics',


    # third-party apps
    'bootstrap_modal_forms',
    'widget_tweaks',
    'crispy_forms',
    'ckeditor',
]

SITE_ID=1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'blog.context_processors.globalVariable', # blog context
            ],
            'libraries': {
                'to_and': 'blog.templatetags.to_and',

            }
        },
    },
]


AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)
WSGI_APPLICATION = 'app.wsgi.application'





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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
CRISPY_TEMPLATE_PACK = 'bootstrap3'
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
STATIC_ROOT=os.path.join(BASE_DIR,'staticfiles')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


AUTH_USER_MODEL='authentication.User'


# SMTP Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST='smtp.gmail.com'
EMAIL_PORT='587'
EMAIL_USE_TLS=True
EMAIL_HOST_USER='winlinmactutorials@gmail.com'
EMAIL_HOST_PASSWORD='obwgivsypubdhjwh'


LOGIN_REDIRECT_URL='/'


GEOIP_PATH =os.path.join(BASE_DIR, 'geoip')
DJANGO_ALLOW_ASYNC_UNSAFE = False



  # 'default': {
  #       'ENGINE': 'django.db.backends.sqlite3',
  #       'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
  #   }
  #   'default': {
  #       'ENGINE': 'django.db.backends.mysql',
  #       'NAME': env('MYSQL_DATABASE'),
  #       'USER': env('MYSQL_USER'),
  #       'PASSWORD': env('MYSQL_PASSWORD'),
  #       'HOST': env('MYSQL_HOST'),
  #       'PORT': env('MYSQL_PORT')
  #   }
    # postgresql connection
    
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
    }
}
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



# runserver.default_port = os.environ.get('SYSTEM_DEFAULT_PORT')
