from typing import ClassVar

from django.contrib import admin

from movieclub.releases.models import Genre, Release


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Admin for Genre model."""

    ordering: ClassVar = ["name"]


@admin.register(Release)
class ReleaseAdmin(admin.ModelAdmin):
    """Admin for Release model."""

    date_hierarchy = "release_date"

    list_filter: ClassVar = ["category"]

    ordering: ClassVar = ["title"]
