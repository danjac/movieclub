from typing import ClassVar

from django.contrib import admin

from movieclub.credits.models import Person


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    """Admin for Person."""

    search_fields: ClassVar = ["name"]
