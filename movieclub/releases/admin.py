from typing import ClassVar

from django.contrib import admin

from movieclub.releases.models import Genre, Release


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Admin for Genre model."""


@admin.register(Release)
class ReleaseAdmin(admin.ModelAdmin):
    """Admin for Release model."""

    list_filter: ClassVar = ["category"]
