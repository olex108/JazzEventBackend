from pathlib import Path

from dotenv import load_dotenv

import os


load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG", "False") == "True"

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")

if not DEBUG:
    raw_origins = os.getenv("CSRF_TRUSTED_ORIGINS", "")
    CSRF_TRUSTED_ORIGINS = raw_origins.split(",") if raw_origins else []

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # services
    "django_vite",

    # libraries
    "sorl.thumbnail",
    "widget_tweaks",
    "phonenumber_field",
    "django_filters",
    "adminsortable2",
    # apps
    "content",
    "users",

    "django_cleanup",
    'debug_toolbar',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",

    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INTERNAL_IPS = [
    "127.0.0.1",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv('DB_HOST', 'db'),
        "PORT": os.getenv('DB_PORT', '5432'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "console_formater": {
            "format": "{asctime}|{levelname}|{module}|{message}",
            "style": "{",
        },
        "file_formater": {
            "format": "{asctime}|{levelname}|{module}|{message}",
            "style": "{"
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "console_formater",
        },
        "message_file": {
            "class": "logging.FileHandler",
            "formatter": "file_formater",
            "filename": BASE_DIR / "logs" / "message.log",
        },
        "users_file": {
            "class": "logging.FileHandler",
            "formatter": "file_formater",
            "filename": BASE_DIR / "logs" / "users.log",
        },
        "stats_file": {
            "class": "logging.FileHandler",
            "formatter": "file_formater",
            "filename": BASE_DIR / "logs" / "stats.log",
        },
    },
    "loggers": {
        "users": {
            "handlers": ["console", "users_file"],
            "level": "INFO",
            "propagate": True,
        },
        "messages": {
            "handlers": ["console", "message_file"],
            "level": "INFO",
            "propagate": True,
        },
        "stats": {
            "handlers": ["stats_file"],
            "level": "INFO",
            "propagate": True,
        }
    },
}

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"

STATICFILES_DIRS = [BASE_DIR / 'static']

STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Опционально: использовать ImageMagick или Pillow (по умолчанию Pillow)
THUMBNAIL_PREFIX = 'thumbnails/'

AUTH_USER_MODEL = "users.User"
LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/users/user_update"
LOGOUT_REDIRECT_URL = "/event/home"


# Email settings
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = os.getenv("EMAIL_ADDRESS")
EMAIL_HOST_PASSWORD = os.getenv("APP_EMAIL_PASSWORD")
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

DJANGO_VITE = {
    "default": {
        "dev_mode": DEBUG,
        "manifest_path": BASE_DIR / "static" / "dist" / "manifest.json",
        "dev_server_host": "localhost",
        "dev_server_port": 3000,
        "static_url_prefix": "dist",
    }
}
