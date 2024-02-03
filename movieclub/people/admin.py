from typing import ClassVar

from django.contrib import admin

from movieclub.people.models import Person


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    """Admin for Person."""

    search_fields: ClassVar = ["name"]
