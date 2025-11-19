import os
from pathlib import Path
from dotenv import load_dotenv
from decouple import config
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
env_path = BASE_DIR / ".env"
if env_path.exists():
    load_dotenv(env_path)

# ----------------------
# SECURITY
# ----------------------
SECRET_KEY = config("DJANGO_SECRET_KEY", default="insecure-key")
DEBUG = config("DJANGO_DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = [
    "localhost", "127.0.0.1",
    "omriturkishbackend.pythonanywhere.com",
]

# ----------------------
# APPLICATIONS
# ----------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party
    'rest_framework',
    'corsheaders',
    'rest_framework.authtoken',
    'rest_framework_simplejwt.token_blacklist',

    # Local apps
    'api',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ----------------------
# CORS / CSRF
# ----------------------
CORS_ALLOWED_ORIGINS = [
    "https://omri-turkish-construction.vercel.app",
    "http://localhost:5173",  # frontend local
]

CSRF_TRUSTED_ORIGINS = [
    "https://omri-turkish-construction.vercel.app",
    "https://omriturkishbackend.pythonanywhere.com",
]

# ----------------------
# URLS & WSGI
# ----------------------
ROOT_URLCONF = 'turkish_backend.urls'

#------------------------------
# REST FRAMEWORK AND JWT
#------------------------------
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',  # utile pour admin
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    )
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,
}

#------------------------
# TEMPLATES
#------------------------

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'turkish_backend.wsgi.application'

# ----------------------
# DATABASES
# ----------------------
# if config("DJANGO_ENV", default="local") == "production":
#     # Base de données sur PythonAnywhere
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.mysql',
#             'NAME': 'omriturkishbacke$default',
#             'USER': 'omriturkishbacke',
#             'PASSWORD': config("Bonjour123", default=""),
#             'HOST': 'omriturkishbackend.mysql.pythonanywhere-services.com',
#             'PORT': '3306',
#             "OPTIONS": {"init_command": "SET sql_mode='STRICT_TRANS_TABLES'"},
#         }
#     }
# else:
#     # Base de données locale (XAMPP)
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.mysql',
#             'NAME': 'turkish_db',
#             'USER': 'root',
#             'PASSWORD': '',
#             'HOST': 'localhost',
#             'PORT': '3306',
#             "OPTIONS": {"init_command": "SET sql_mode='STRICT_TRANS_TABLES'"},
#         }
#     }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config("DB_NAME"),
        'USER': config("DB_USER"),
        'PASSWORD': config("DB_PASSWORD", default=""),
        'HOST': config("DB_HOST", default="127.0.0.1"),
        'PORT': config("DB_PORT", default="3306"),
        "OPTIONS": {"init_command": "SET sql_mode='STRICT_TRANS_TABLES'"},
    }
}


# ----------------------
# PASSWORDS
# ----------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ----------------------
# INTERNATIONALIZATION
# ----------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ----------------------
# STATIC & MEDIA
# ----------------------
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ----------------------
# DEFAULT FIELD
# ----------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
