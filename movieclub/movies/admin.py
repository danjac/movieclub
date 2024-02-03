from typing import ClassVar

from django.contrib import admin

from movieclub.movies.models import CastMember, CrewMember, Genre, Movie


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Movie admin."""

    ordering: ClassVar = ["name"]


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """Movie admin."""

    date_hierarchy: ClassVar = "release_date"
    search_fields: ClassVar = ["title"]


@admin.register(CastMember)
class CastMemberAdmin(admin.ModelAdmin):
    """Cast members admin."""

    list_display: ClassVar = ["movie", "character", "person", "order"]
    list_select_related: ClassVar = True
    raw_id_fields: ClassVar = ["movie", "person"]
    search_fields: ClassVar = ["movie__title", "person__name"]


@admin.register(CrewMember)
class CrewMemberAdmin(admin.ModelAdmin):
    """Crew members admin."""

    list_display: ClassVar = ["movie", "job", "person"]
    list_select_related: ClassVar = True
    raw_id_fields: ClassVar = ["movie", "person"]
    search_fields: ClassVar = ["movie__title", "person__name"]
