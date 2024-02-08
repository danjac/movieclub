from typing import ClassVar

from django.contrib import admin

from movieclub.activitypub.models import Actor, Instance


@admin.register(Instance)
class InstanceAdmin(admin.ModelAdmin):
    """Admin for Instance."""

    list_display: ClassVar = ["domain", "local"]


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    """Admin for Instance."""

    list_display: ClassVar = ["handle", "instance", "user"]
    list_select_related: ClassVar = True
    raw_id_fields: ClassVar = ["instance", "user"]
