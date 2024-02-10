import pathlib
from email.utils import getaddresses

import environ
import sentry_sdk
from django.urls import reverse_lazy
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import ignore_logger

env = environ.Env(
    # should be one of "mandatory", "optional" or "none"
    ACCOUNT_EMAIL_VERIFICATION=(str, "none"),
    ADMIN_SITE_HEADER=(str, "Movieclub Admin"),
    ADMIN_URL=(str, "admin/"),
    ADMINS=(list, []),
    ALLOWED_HOSTS=(list, ["127.0.0.1", "localhost"]),
    CONN_MAX_AGE=(int, 360),
    DATABASE_URL=(str, "postgresql://postgres:password@127.0.0.1:5432/postgres"),
    DEBUG=(bool, False),
    EMAIL_URL=(str, "smtp://127.0.0.1:1025"),
    INVITATIONS_INVITATION_ONLY=(bool, True),
    MAILGUN_API_KEY=(str, ""),
    # For European domains: https://api.eu.mailgun.net/v3
    MAILGUN_API_URL=(str, "https://api.mailgun.net/v3"),
    REDIS_URL=(str, "redis://127.0.0.1:6379/0"),
    SECRET_KEY=(
        str,
        "django-insecure-a&tm18c2sd$gv@ah7gv3!ts#@hhi=@ojsc%&ddmc21m1u-b_8z",
    ),
    SENTRY_URL=(str, ""),
    STATIC_URL=(str, "/static/"),
    TEMPLATE_DEBUG=(bool, False),
    TMDB_API_ACCESS_TOKEN=(str, ""),
    USER_AGENT=(str, "movieclub/0.0.0"),
    USE_BROWSER_RELOAD=(bool, False),
    USE_COLLECTSTATIC=(bool, True),
    USE_DEBUG_TOOLBAR=(bool, False),
    USE_FASTDEV=(bool, False),
    USE_HSTS=(bool, False),
    USE_HTTPS=(bool, True),
)

BASE_DIR = pathlib.Path(__file__).resolve(strict=True).parents[1]

environ.Env.read_env(BASE_DIR / ".env")

DEBUG = env("DEBUG")

SECRET_KEY = env("SECRET_KEY")

INSTALLED_APPS: list[str] = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.postgres",
    "django.contrib.sessions",
    "django.contrib.sitemaps",
    "django.contrib.sites",
    "django.contrib.staticfiles",
    "django.forms",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "django_extensions",
    "django_htmx",
    "django_rq",
    "health_check",
    "health_check.db",
    "health_check.cache",
    "health_check.contrib.migrations",
    "health_check.contrib.psutil",
    "health_check.contrib.redis",
    "heroicons",
    "invitations",
    "template_partials",
    "widget_tweaks",
    "movieclub.activitypub",
    "movieclub.movies",
    "movieclub.people",
    "movieclub.reviews",
    "movieclub.users",
]


MIDDLEWARE: list[str] = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django_permissions_policy.PermissionsPolicyMiddleware",
    "django.contrib.sites.middleware.CurrentSiteMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.gzip.GZipMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.common.BrokenLinkEmailsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
    "movieclub.middleware.CacheControlMiddleware",
    "movieclub.middleware.HtmxMessagesMiddleware",
    "movieclub.middleware.HtmxRedirectMiddleware",
]

# Databases

CONN_MAX_AGE = env("CONN_MAX_AGE")

DATABASES = {
    "default": env.db()
    | {
        "ATOMIC_REQUESTS": True,
        "CONN_MAX_AGE": CONN_MAX_AGE,
        "CONN_HEALTH_CHECKS": CONN_MAX_AGE > 0,
        "OPTIONS": {
            "options": "-c statement_timeout=30s",
        },
    }
}

# Caches


CACHES = {
    "default": env.cache("REDIS_URL", backend="django_redis.cache.RedisCache")
    | {
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "IGNORE_EXCEPTIONS": True,
        }
    }
}

# Templates

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "OPTIONS": {
            "builtins": [
                # "movieclub.template",
            ],
            "debug": env("TEMPLATE_DEBUG"),
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]

# https://github.com/boxed/django-fastdev
if USE_FASTDEV := env("USE_FASTDEV"):
    INSTALLED_APPS += ["django_fastdev"]
    FASTDEV_STRICT_TEMPLATE_CHECKING = True

# prevent deprecation warnings
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Server settings

ROOT_URLCONF = "movieclub.urls"

ALLOWED_HOSTS: list[str] = env("ALLOWED_HOSTS")

# User-Agent header for API calls from this site
USER_AGENT = env("USER_AGENT")

SITE_ID = 1

# Session and cookies

SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"

CSRF_USE_SESSIONS = True

SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True

# Email configuration

EMAIL_CONFIG = env.email_url()
EMAIL_HOST = EMAIL_CONFIG["EMAIL_HOST"]


# Mailgun
# https://anymail.dev/en/v9.0/esps/mailgun/

if MAILGUN_API_KEY := env("MAILGUN_API_KEY"):
    INSTALLED_APPS += ["anymail"]

    EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"

    MAILGUN_API_URL = env("MAILGUN_API_URL")

    ANYMAIL = {
        "MAILGUN_API_KEY": MAILGUN_API_KEY,
        "MAILGUN_API_URL": MAILGUN_API_URL,
        "MAILGUN_SENDER_DOMAIN": EMAIL_HOST,
    }
else:
    vars().update(EMAIL_CONFIG)

ADMINS = getaddresses(env("ADMINS"))

DEFAULT_FROM_EMAIL = env.str("DEFAULT_FROM_EMAIL", default=f"no-reply@{EMAIL_HOST}")
SERVER_EMAIL = env.str("SERVER_EMAIL", default=f"errors@{EMAIL_HOST}")
SUPPORT_EMAIL = env.str("SUPPORT_EMAIL", default=f"support@{EMAIL_HOST}")

# authentication settings
# https://docs.djangoproject.com/en/dev/ref/settings/#authentication-backends

AUTH_USER_MODEL = "users.User"

# Invitations
# https://django-invitations.readthedocs.io/en/latest/usage.html

ACCOUNT_ADAPTER = "invitations.models.InvitationsAdapter"

INVITATIONS_INVITATION_ONLY = env("INVITATIONS_INVITATION_ONLY")


AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

AUTH_PASSWORD_VALIDATORS: list[dict[str, str]] = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LOGIN_REDIRECT_URL = reverse_lazy("landing_page")

LOGIN_URL = "account_login"

# https://django-allauth.readthedocs.io/en/latest/configuration.html

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_LOGIN_ON_PASSWORD_RESET = True
ACCOUNT_PREVENT_ENUMERATION = True
ACCOUNT_AUTHENTICATION_METHOD = "username_email"

ACCOUNT_EMAIL_VERIFICATION = env("ACCOUNT_EMAIL_VERIFICATION")

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        },
    }
}

# admin settings

ADMIN_URL = env("ADMIN_URL")

ADMIN_SITE_HEADER = env("ADMIN_SITE_HEADER")

# Internationalization/Localization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = "en"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files

STATIC_URL = env("STATIC_URL")
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# Whitenoise
# https://whitenoise.readthedocs.io/en/latest/django.html
#

if USE_COLLECTSTATIC := env("USE_COLLECTSTATIC"):
    STORAGES = {
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }
else:
    # for development only
    INSTALLED_APPS += ["whitenoise.runserver_nostatic"]


# Templates
# https://docs.djangoproject.com/en/1.11/ref/forms/renderers/

FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

# Secure settings
# https://docs.djangoproject.com/en/4.1/topics/security/

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

if USE_HTTPS := env("USE_HTTPS"):
    SECURE_PROXY_SSL_HEADER = tuple(
        env.str(
            "SECURE_PROXY_SSL_HEADER", default="HTTP_X_FORWARDED_PROTO, https"
        ).split(","),
    )
    SECURE_SSL_REDIRECT = True

# Make sure to enable USE_HSTS if your load balancer is not using HSTS in production,
# otherwise leave disabled.

if USE_HSTS := env("USE_HSTS"):
    SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool(
        "SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True
    )
    SECURE_HSTS_PRELOAD = env.bool("SECURE_HSTS_PRELOAD", default=True)
    SECURE_HSTS_SECONDS = env.int("SECURE_HSTS_SECONDS", default=15768001)
#
# Permissions Policy
# https://pypi.org/project/django-permissions-policy/

PERMISSIONS_POLICY: dict[str, list] = {
    "accelerometer": [],
    "ambient-light-sensor": [],
    "camera": [],
    "document-domain": [],
    "encrypted-media": [],
    "fullscreen": [],
    "geolocation": [],
    "gyroscope": [],
    "magnetometer": [],
    "microphone": [],
    "payment": [],
    "usb": [],
}

# Logging

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
        "null": {"level": "DEBUG", "class": "logging.NullHandler"},
    },
    "loggers": {
        "root": {
            "handlers": ["console"],
            "level": "INFO",
        },
        "django.server": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "django.security.DisallowedHost": {
            "handlers": ["null"],
            "propagate": False,
        },
        "django.request": {
            "level": "CRITICAL",
            "propagate": False,
        },
        "httpx": {
            "handlers": ["console"],
            "level": "CRITICAL",
            "propagate": False,
        },
        "httpcore": {
            "handlers": ["console"],
            "level": "CRITICAL",
            "propagate": False,
        },
    },
}

# Health checks
# https://pypi.org/project/django-health-check/

HEALTH_CHECK = {
    "DISK_USAGE_MAX": 90,  # percent
    "MEMORY_MIN": 100,  # in MB
}

# Django-RQ
# https://github.com/rq/django-rq

RQ_QUEUES = {
    "default": {
        "URL": env("REDIS_URL"),
    }
}

RQ_SHOW_ADMIN_LINK = True

# Sentry
# https://docs.sentry.io/platforms/python/guides/django/

if SENTRY_URL := env.str("SENTRY_URL"):
    ignore_logger("django.security.DisallowedHost")

    sentry_sdk.init(
        dsn=SENTRY_URL,
        integrations=[DjangoIntegration()],
        traces_sample_rate=0.5,
        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True,
    )

# Django browser reload
# https://github.com/adamchainz/django-browser-reload

if USE_BROWSER_RELOAD := env("USE_BROWSER_RELOAD"):
    INSTALLED_APPS += ["django_browser_reload"]

    MIDDLEWARE += ["django_browser_reload.middleware.BrowserReloadMiddleware"]

# Debug toolbar
# https://github.com/jazzband/django-debug-toolbar

if USE_DEBUG_TOOLBAR := env("USE_DEBUG_TOOLBAR"):
    INSTALLED_APPS += ["debug_toolbar"]

    MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

    # INTERNAL_IPS required for debug toolbar
    INTERNAL_IPS = env.list("INTERNAL_IPS", default=["127.0.0.1"])


# Project-specific settings

TMDB_API_ACCESS_TOKEN = env("TMDB_API_ACCESS_TOKEN")
