from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from movieclub import views

admin.site.site_header = settings.ADMIN_SITE_HEADER


urlpatterns = [
    path("", views.landing_page, name="landing_page"),
    path("", include("movieclub.activitypub.urls")),
    path("movies/", include("movieclub.movies.urls")),
    path("account/", include("allauth.urls")),
    path("invitations/", include("invitations.urls")),
    path("ht/", include("health_check.urls")),
    path("rq/", include("django_rq.urls")),
    path(settings.ADMIN_URL, admin.site.urls),
]

if "django_browser_reload" in settings.INSTALLED_APPS:  # pragma: no cover
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
    ]

if "debug_toolbar" in settings.INSTALLED_APPS:  # pragma: no cover
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]
