 
import os
import sys
import json
from pathlib import Path 
from dotenv import load_dotenv
from datetime import timedelta
from django.utils.translation import gettext_lazy as _
load_dotenv()


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-q!%=dpzq(2pfmn$uk(=+#zkz%&gsn)lpg30ejpi&ufl_h9e17x'
SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = os.getenv('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = [
    'localhost',
    f"{os.getenv('MAIN_DOMAIN')}",
    f"{os.getenv('MAIN_DOMAIN')}:{os.getenv('DJANGO_APP_PORT')}",
    f"{os.getenv('MAIN_DOMAIN')}:{os.getenv('NGINX_APP_PORT')}",
    f"{os.getenv('MAIN_DOMAIN')}:{os.getenv('PSQL_PORT')}",
    f"{os.getenv('MAIN_DOMAIN')}:{os.getenv('REDIS_PORT')}"
]
#default
INSTALLED_APPS = [
    "admin_interface",
    "colorfield",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django_countries',
    # allauth
    'allauth',
    'allauth.account',
    # 'allauth.socialaccount',
    # 'allauth.socialaccount.providers.google',
    # 'allauth.socialaccount.providers.facebook',
    'pwa',
    # MODELS
    'polymorphic',  
    # DREST
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    # THEME
    'crispy_forms',
    # JSON, CSV, JSON, XML
    'import_export',
    # CUSTOM APPS
    'core',
    'api',
    'persons',
    'social',
    'users',
    'authentication',
]

# CSRF (Cross-Site Request Forgery)
CSRF_COOKIE_SECURE = not DEBUG

CSRF_TRUSTED_ORIGINS = [
    f"{os.getenv('PROTOCOL')}://{os.getenv('MAIN_DOMAIN')}:{os.getenv('DJANGO_APP_PORT')}",
    f"{os.getenv('PROTOCOL')}://{os.getenv('MAIN_DOMAIN')}:{os.getenv('REACT_APP_PORT')}",
    f"{os.getenv('PROTOCOL')}://{os.getenv('MAIN_DOMAIN')}:{os.getenv('NGINX_APP_PORT')}",
    f"{os.getenv('PROTOCOL')}://{os.getenv('MAIN_DOMAIN')}:{os.getenv('PSQL_PORT')}",
    f"{os.getenv('PROTOCOL')}://{os.getenv('MAIN_DOMAIN')}:{os.getenv('REDIS_PORT')}",
    f"{os.getenv('PROTOCOL')}://{os.getenv('MAIN_DOMAIN')}",
]

# CORS (Cross-Origin Resource Sharing)
CORS_ALLOW_ALL_ORIGINS = DEBUG
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    f"{os.getenv('PROTOCOL')}://{os.getenv('MAIN_DOMAIN')}:{os.getenv('DJANGO_APP_PORT')}",
    f"{os.getenv('PROTOCOL')}://{os.getenv('MAIN_DOMAIN')}:{os.getenv('REACT_APP_PORT')}",
    f"{os.getenv('PROTOCOL')}://{os.getenv('MAIN_DOMAIN')}:{os.getenv('NGINX_APP_PORT')}",
    f"{os.getenv('PROTOCOL')}://{os.getenv('MAIN_DOMAIN')}:{os.getenv('PSQL_PORT')}",
    f"{os.getenv('PROTOCOL')}://{os.getenv('MAIN_DOMAIN')}:{os.getenv('REDIS_PORT')}",
    f"{os.getenv('PROTOCOL')}://{os.getenv('MAIN_DOMAIN')}",
]

X_FRAME_OPTIONS = "SAMEORIGIN"
SILENCED_SYSTEM_CHECKS = ["security.W019"]

SITE_ID = 1
AUTH_USER_MODEL = 'users.User'

REST_FRAMEWORK = {
    # 'DEFAULT_PERMISSION_CLASSES': [
    #     'rest_framework.permissions.IsAuthenticated',
    # ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema'
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
}
 
MIDDLEWARE_CLASSES = [
    'livereload.middleware.LiveReloadScript',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Whitenoise
    'django.middleware.locale.LocaleMiddleware',  # Multi-Language
    'corsheaders.middleware.CorsMiddleware',  # corsheaders
    'allauth.account.middleware.AccountMiddleware', # allauth
]

ROOT_URLCONF = f"{os.getenv('APP_NAME')}.urls"

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': f"redis://{os.getenv('MAIN_DOMAIN')}:{os.getenv('REDIS_PORT')}/0", 
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            # "SOCKET_CONNECT_TIMEOUT": 5,  # seconds
            # "SOCKET_TIMEOUT": 5,  # seconds
        }
    }
}
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / f"{os.getenv('APP_NAME')}/templates",
        ],
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

# allauth
AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

WSGI_APPLICATION = f"{os.getenv('APP_NAME')}.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': os.getenv('PSQL_ENGINE'),
        'NAME': os.getenv('PSQL_NAME'),
        'USER': os.getenv('PSQL_USER'),
        'PASSWORD': os.getenv('PSQL_PASSWORD'),
        'HOST': os.getenv('PSQL_HOST'), 
        'PORT': os.getenv('PSQL_PORT'),  
    },
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

if DEBUG:
    AUTH_PASSWORD_VALIDATORS.append(
        {
            'NAME': 'django.contrib.auth.password_validation.UserBlacklistValidator',
        },
    )

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

# TIME ZONE

LANGUAGE_CODE = os.getenv('LANGUAGE_CODE')

TIME_ZONE = os.getenv('TZ')

USE_I18N = True

USE_L10N = True

USE_TZ = True
# PROJECT DIRECTORIES
 
PROJECT_ROOT = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'apps'))

PARLER_DEFAULT_LANGUAGE_CODE = os.getenv('LANGUAGE_CODE')

PARLER_LANGUAGES = {
    # Global site
    1: (
        {'code': 'en-US',},
        {'code': 'es-MX',},
    ),
    # MX site
    2: (
        {'code': 'es-mx',},
    ),
    # US site
    3: (
        {'code': 'en-US',},
    ),
    'default': {
        'fallback': os.getenv('LANGUAGE_CODE'),  
        'hide_untranslated': False,  
    }
}

LANGUAGES = [
    ('en-US', _('English')),
    ('es-MX', _('Español (México)')),
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale/en-US/LC_MESSAGES'),
    os.path.join(BASE_DIR, 'locale/es-MX/LC_MESSAGES'),
]
PARLER_SHOW_EXCLUDED_LANGUAGE_TABS = True
PARLER_DEFAULT_ACTIVATE = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_TMP = os.path.join(BASE_DIR, 'static')

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

os.makedirs(STATIC_TMP, exist_ok=True)
os.makedirs(STATIC_ROOT, exist_ok=True)

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'media'),
] 

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# PWA

PWA_SERVICE_WORKER_PATH = os.path.join(BASE_DIR, 'static/js', 'serviceworker.js')
PWA_APP_NAME = os.getenv('APP_NAME')
PWA_APP_DESCRIPTION = os.getenv('APP_DESCRIPTION')
PWA_APP_THEME_COLOR = '#18181B'
PWA_APP_BACKGROUND_COLOR = '#27272A'
PWA_APP_DISPLAY = 'standalone'
PWA_APP_SCOPE = '/'
PWA_APP_ORIENTATION = 'any'
PWA_APP_START_URL = '/'
PWA_APP_STATUS_BAR_COLOR = 'default'
PWA_APP_ICONS = [
    {
        'src': 'static/images/icons/icon-160x160.png',
        'sizes': '160x160'
    }
]
PWA_APP_ICONS_APPLE = [
    {
        'src': 'static/images/icons/icon-160x160.png',
        'sizes': '160x160'
    }
]
PWA_APP_SPLASH_SCREEN = [
    {
        'src': 'static/images/icons/icon.png',
        'media': '(device-width: 320px) and (device-height: 568px) and (-webkit-device-pixel-ratio: 2)'
    }
]
PWA_APP_DIR = 'ltr'
PWA_APP_LANG = os.getenv('LANGUAGE_CODE')

# AUTH

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/'
SOCIALACCOUNT_QUERY_EMAIL = True
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_SESSION_REMEMBER = True

# Ruta al archivo JSON
allauth_json = os.path.join(
    BASE_DIR, 'data/json/', 'allauth.json')

# Verificar si el archivo existe y no está vacío
if os.path.exists(allauth_json) and os.path.getsize(allauth_json) > 0:
    # Cargar el contenido del archivo JSON
    with open(allauth_json, 'r') as file:
        allauth_content = file.read()
    # Analizar el contenido JSON
    allauth_list = json.loads(allauth_content)
    SOCIALACCOUNT_PROVIDERS = allauth_list
else:
    SOCIALACCOUNT_PROVIDERS = {}

# Agregar la lista de contenido inapropiado a configuraciones
usernames_blacklist_json = os.path.join(
    BASE_DIR, 'data/json/', 'usernames_blacklist.json')

# Verificar si el archivo existe y no está vacío
if os.path.exists(usernames_blacklist_json) and os.path.getsize(usernames_blacklist_json) > 0:
    with open(usernames_blacklist_json, 'r') as file:
        usernames_blacklist_content = file.read()
    innapropiate_list = json.loads(usernames_blacklist_content)
    ACCOUNT_USERNAME_BLACKLIST = innapropiate_list
else:
    ACCOUNT_USERNAME_BLACKLIST = []

ACCOUNT_USER_MODEL_USERNAME_FIELD = 'username'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'none'


# EMAILEMAIL_BACKEND = os.getenv('EMAIL_BACKEND')
# EMAIL_HOST = os.getenv('EMAIL_HOST')
# EMAIL_PORT = os.getenv('EMAIL_PORT')
# EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS')
# EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
# DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')
# SERVER_EMAIL = os.getenv('SERVER_EMAIL')