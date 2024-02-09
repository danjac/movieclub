from __future__ import annotations

import uuid
from typing import ClassVar

from django.conf import settings
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


class Follow(TimeStampedModel):
    """Tracks following remote or local actors.

    When creating a local follow, we can skip ActivityPub and just
    handle the transaction in local database.

    For a remote follow, we need to run a task to create an AP object
    and send that object to the remote Actor's inbox.

    We then need to handle (through local user Inbox) the Accepted or Rejected
    action.

    In either case, the status is Requested until Accepted or Rejected.
    """

    class Status(models.TextChoices):
        REQUESTED = "requested", "Requested"
        ACCEPTED = "accepted", "Accepted"
        REJECTED = "rejected", "Rejected"

    follower_local = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="followed",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    follower_remote = models.ForeignKey(
        Actor,
        related_name="followed",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    followed_local = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="local_followers",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    followed_remote = models.ForeignKey(
        Actor,
        related_name="remote_followers",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    activity_object_id = models.UUIDField(unique=True, default=uuid.uuid4)

    status = models.CharField(max_length=15, default=Status.REQUESTED)

    class Meta:
        constraints: ClassVar = [
            # must be either local or remote, not both
            models.CheckConstraint(
                check=models.Q(
                    models.Q(
                        followed_local__isnull=False,
                        followed_remote__isnull=True,
                    )
                    | models.Q(
                        followed_local__isnull=True,
                        followed_remote__isnull=False,
                    )
                ),
                name="%(app_label)s_%(class)s_must_be_either_local_or_remote",
            ),
            models.UniqueConstraint(
                fields=["follower_local", "followed_local"],
                name="%(app_label)s_%(class)s_unique_follow_local_to_local",
                condition=models.Q(
                    followed_local__isnull=False,
                    follower_local__isnull=False,
                ),
            ),
            models.UniqueConstraint(
                fields=["follower_local", "followed_remote"],
                name="%(app_label)s_%(class)s_unique_follow_local_to_remote",
                condition=models.Q(
                    followed_remote__isnull=False,
                    follower_local__isnull=False,
                ),
            ),
            models.UniqueConstraint(
                fields=["follower_remote", "followed_local"],
                name="%(app_label)s_%(class)s_unique_follow_remote_to_local",
                condition=models.Q(
                    followed_local__isnull=False,
                    follower_remote__isnull=False,
                ),
            ),
        ]
