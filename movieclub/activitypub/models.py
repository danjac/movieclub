from typing import ClassVar

from django.conf import settings
from django.db import models
from model_utils.models import TimeStampedModel


class Instance(TimeStampedModel):
    """A Federated instance."""

    domain = models.CharField(max_length=120, unique=True)
    local = models.BooleanField(default=True)
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

    handle = models.CharField(max_length=120, blank=True)
    name = models.CharField(max_length=120, blank=True)
    summary = models.TextField(blank=True)

    actor_type = models.CharField(max_length=15, default=ActorType.PERSON)

    # for a Local instance user
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        related_name="actor",
        on_delete=models.SET_NULL,
    )

    # TBD: when we have Groups, those will also be Actors.

    # blocked for all users: each user will have own block list
    blocked = models.BooleanField(default=False)

    # for Remote instances
    profile_url = models.URLField(blank=True)
    outbox_url = models.URLField(blank=True)
    inbox_url = models.URLField(blank=True)

    # for Local instances
    private_key = models.TextField(blank=True)
    public_key = models.TextField(blank=True)

    class Meta:
        constraints: ClassVar = [
            models.UniqueConstraint(
                fields=["instance", "handle"],
                name="%(app_label)s_%(class)s_unique_handle",
                condition=~models.Q(handle=""),
            ),
            models.UniqueConstraint(
                fields=["instance", "user"],
                name="%(app_label)s_%(class)s_unique_local_user",
                condition=models.Q(user__isnull=False),
            ),
        ]


class Following(TimeStampedModel):
    """Tracks following actors."""

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
                condition=~models.Q(handle=""),
            ),
        ]

    def __str__(self) -> str:
        """Returns status"""
        return self.status
