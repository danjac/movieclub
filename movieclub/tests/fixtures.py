from collections.abc import Callable, Generator

import pytest
from django.conf import Settings
from django.contrib.sites.models import Site
from django.core.cache import cache
from django.http import HttpRequest, HttpResponse


@pytest.fixture()
def site():
    return Site.objects.get_current()


@pytest.fixture(autouse=True)
def _settings_overrides(settings: Settings) -> None:
    """Default settings for all tests."""
    settings.ALLOWED_HOSTS = ["example.com", "testserver", "localhost"]
    settings.CACHES = {
        "default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"}
    }
    settings.LOGGING = None
    settings.PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
    settings.MOVIECLUB_TMDB_API_KEY = "NOTSET"


@pytest.fixture()
def _locmem_cache(settings: Settings) -> Generator:
    settings.CACHES = {
        "default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}
    }
    yield
    cache.clear()


@pytest.fixture(scope="session")
def get_response() -> Callable[[HttpRequest], HttpResponse]:
    return lambda req: HttpResponse()
