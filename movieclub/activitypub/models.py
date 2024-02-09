from __future__ import annotations

from typing import ClassVar

from django.db import models
from model_utils.models import TimeStampedModel


class Instance(TimeStampedModel):
    """A Federated instance."""

    domain = models.CharField(max_length=120, unique=True)
    blocked = models.BooleanField(default=False)

    def __str__(self) -> str:
        """Return the domain."""
        return self.domain


class Actor(TimeStampedModel):
    """ActivityPub Actor."""

    class ActorType(models.TextChoices):
        # For now we just have "Person"
        PERSON = "person", "Person"
        GROUP = "group", "Group"
        SERVICE = "service", "Service"
        APPLICATION = "application", "Application"
        ORGANIZATION = "organization", "Organization"

    instance = models.ForeignKey(
        Instance, on_delete=models.PROTECT, related_name="actors"
    )
    # for a Remote instance

    handle = models.CharField(max_length=120)
    name = models.CharField(max_length=120, blank=True)
    summary = models.TextField(blank=True)

    actor_type = models.CharField(
        max_length=15,
        default=ActorType.PERSON,
        choices=ActorType,
    )

    # blocked for all users: each user will have own block list
    blocked = models.BooleanField(default=False)

    # for Remote instances
    profile_url = models.URLField()
    outbox_url = models.URLField()
    inbox_url = models.URLField()

    class Meta:
        constraints: ClassVar = [
            models.UniqueConstraint(
                fields=["instance", "handle"],
                name="%(app_label)s_%(class)s_unique_handle",
                condition=~models.Q(handle=""),
            ),
        ]

    def __str__(self) -> str:
        """Return handle"""
        return self.handle

    def get_resource(self) -> str:
        """Returns name@domain"""
        return f"{self.handle}@{self.instance.domain}"


class Following(TimeStampedModel):
    """Tracks following actors.

    TBD: we should have RemoteFollow and LocalFollow models.
    RemoteFollow should have FK to Actor, and LocalFollow to User.
    """

    class Status(models.TextChoices):
        REQUESTED = "requested", "Requested"
        ACCEPTED = "accepted", "Accepted"
        REJECTED = "rejected", "Rejected"

    follower = models.ForeignKey(
        Actor, related_name="following", on_delete=models.CASCADE
    )
    followed = models.ForeignKey(
        Actor, related_name="followers", on_delete=models.CASCADE
    )

    status = models.CharField(max_length=15, default=Status.REQUESTED)

    class Meta:
        constraints: ClassVar = [
            models.UniqueConstraint(
                fields=["follower", "followed"],
                name="%(app_label)s_%(class)s_unique_following",
            ),
        ]
