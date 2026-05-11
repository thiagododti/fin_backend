from __future__ import annotations

import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv


# =============================================================================
# 1) BASE / ENV HELPERS
# =============================================================================
BASE_DIR = Path(__file__).resolve().parent.parent


def env_bool(name: str, default: bool = False) -> bool:
    return os.getenv(name, "True" if default else "False").lower() in ("1", "true", "yes", "on")


def env_int(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, str(default)))
    except (TypeError, ValueError):
        return default


def env_list(name: str, default: list[str] | None = None) -> list[str]:
    value = os.getenv(name)
    if value is None:
        return list(default or [])
    return [item.strip() for item in value.split(",") if item.strip()]


# =============================================================================
# 2) DOTENV (DEV-ONLY / EXPLICIT)
# =============================================================================
# Em produção/container: use env do Docker (env_file / environment).
# Se quiser usar .env localmente: DJANGO_READ_DOTENV=True
READ_DOTENV = env_bool("DJANGO_READ_DOTENV", default=False) == False
if READ_DOTENV:
    load_dotenv(override=False)


# =============================================================================
# 3) CORE
# =============================================================================
SECRET_KEY = os.getenv("SECRET_KEY", "")
DEBUG = env_bool("DEBUG", default=False)
TESTING = env_bool("TESTING", default=False)

LANGUAGE_CODE = os.getenv("LANGUAGE_CODE", "pt-br")
TIME_ZONE = os.getenv("TIME_ZONE", "America/Sao_Paulo")

USE_I18N = True
USE_TZ = False


# =============================================================================
# 4) HOSTS / PROXY / HTTPS
# =============================================================================
ALLOWED_HOSTS = env_list("ALLOWED_HOSTS", ["localhost", "127.0.0.1"])

ENABLE_HTTPS = env_bool("ENABLE_HTTPS", default=False)
if ENABLE_HTTPS:
    USE_X_FORWARDED_HOST = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = True
    # Mesmo sem cookies de auth, essas configs reforçam segurança se você tiver cookies de qualquer tipo
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True


# =============================================================================
# 5) APPS
# =============================================================================
DJANGO_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.staticfiles",
    "django.contrib.sessions",
]

LOCAL_APPS = [
    "apps.users.apps.UsersConfig",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "rest_framework.authtoken",
    "drf_spectacular",
    "django_filters",
    "simple_history",
]

INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS + THIRD_PARTY_APPS

AUTH_USER_MODEL = "users.User"


# =============================================================================
# 6) MIDDLEWARE (API-only)
# =============================================================================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    # necessário para request.user no Django (e útil mesmo usando DRF)
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",
    "django.middleware.locale.LocaleMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"


# =============================================================================
# 7) TEMPLATES
# =============================================================================
# Mesmo API-only, o Django espera TEMPLATES configurado para algumas partes internas.
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {"context_processors": ["django.template.context_processors.request"]},
    }
]


# =============================================================================
# 8) DATABASE
# =============================================================================
SELECTED_DB = os.getenv("SWITCH_DB")
if SELECTED_DB == "sqlite":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
elif SELECTED_DB == "postgres":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("POSTGRES_DB"),
            "USER": os.getenv("POSTGRES_USER"),
            "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
            "HOST": os.getenv("POSTGRES_HOST"),
            "PORT": os.getenv("POSTGRES_PORT"),
        }
    }


# =============================================================================
# 9) PASSWORD VALIDATORS
# =============================================================================
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# =============================================================================
# 10) STATIC / MEDIA
# =============================================================================
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
if DEBUG:
    MEDIA_ROOT = BASE_DIR / "media"
else:
    MEDIA_ROOT = os.getenv("MEDIA_ROOT", "/vol/web/media")


# =============================================================================
# 11) DRF / AUTH (JWT + Token ONLY)
# =============================================================================
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        # "rest_framework.authentication.TokenAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "EXCEPTION_HANDLER": "config.exceptions.custom_exception_handler",
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=env_int("JWT_ACCESS_MINUTES", 60)),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=env_int("JWT_REFRESH_DAYS", 1)),
    "AUTH_HEADER_TYPES": ("Bearer",),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
}


# =============================================================================
# 12) SWAGGER / OPENAPI
# =============================================================================
SPECTACULAR_SETTINGS = {
    "TITLE": "Automation API",
    "DESCRIPTION": "Projeto de monitoramento de automações com backend desenvolvido em Django e Django REST Framework dedicado exclusivamente a APIs.",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SORT_OPERATION_PARAMETERS": False,
}


# =============================================================================
# 13) CORS (somente se precisar)
# =============================================================================
ENABLE_CORS = env_bool("ENABLE_CORS", default=False)
if ENABLE_CORS:
    INSTALLED_APPS.append("corsheaders")
    MIDDLEWARE.insert(1, "corsheaders.middleware.CorsMiddleware")

    CORS_ALLOWED_ORIGINS = env_list("CORS_ALLOWED_ORIGINS", [])
    CORS_ALLOW_CREDENTIALS = env_bool("CORS_ALLOW_CREDENTIALS", default=False)

    CORS_ALLOW_METHODS = ["DELETE", "GET", "OPTIONS", "PATCH", "POST", "PUT"]
    CORS_ALLOW_HEADERS = [
        "accept",
        "accept-encoding",
        "authorization",
        "content-type",
        "dnt",
        "origin",
        "user-agent",
        "x-requested-with",
    ]


# =============================================================================
# 14) LOGGING mínimo para enxergar DisallowedHost em produção
# =============================================================================
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "loggers": {
        # Isso ajuda MUITO a diagnosticar 400 por host inválido
        "django.security.DisallowedHost": {"handlers": ["console"], "level": "ERROR", "propagate": False},
        "django.request": {"handlers": ["console"], "level": "ERROR", "propagate": True},
    },
}
