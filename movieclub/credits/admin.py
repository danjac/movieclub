from typing import ClassVar

from django.contrib import admin

from movieclub.credits.models import CastMember, CrewMember, Person


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    """Admin for Person."""

    search_fields: ClassVar = ["name"]


@admin.register(CastMember)
class CastMemberAdmin(admin.ModelAdmin):
    """Admin for Person."""

    list_display: ClassVar = ["person", "character"]
    search_fields: ClassVar = ["person__name"]


@admin.register(CrewMember)
class CrewMemberAdmin(admin.ModelAdmin):
    """Admin for Person."""

    list_display: ClassVar = ["person", "job"]
    search_fields: ClassVar = ["person__name"]
