from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from django.conf import settings
from django.db import models
from model_utils.models import TimeStampedModel

from movieclub.activitypub.http_signature import create_key_pair

if TYPE_CHECKING:  # pragma: no cover
    from django.contrib.sites.models import Site

    from movieclub.users.models import User


class InstanceQuerySet(models.QuerySet):
    """QuerySet for Instance."""

    def local(self) -> InstanceQuerySet:
        """Return local instances"""
        return self.filter(local=True)

    def get_for_site(self, site: Site) -> Instance:
        """Return local site matching site domain."""
        return self.get(domain__iexact=site.domain)


class Instance(TimeStampedModel):
    """A Federated instance."""

    domain = models.CharField(max_length=120, unique=True)
    local = models.BooleanField(default=True)
    blocked = models.BooleanField(default=False)

    objects = InstanceQuerySet.as_manager()

    def __str__(self) -> str:
        """Return the domain."""
        return self.domain


class ActorQuerySet(models.QuerySet):
    """QuerySet for Actor."""

    def local(self) -> ActorQuerySet:
        """Returns local actors."""
        return self.filter(instance__local=True)

    def create_for_user(self, user: User, instance: Instance, **kwargs) -> Actor:
        """Creates actor for local instance."""

        priv_key, pub_key = create_key_pair()

        return self.create(
            user=user,
            handle=user.username,
            instance=instance,
            private_key=priv_key,
            public_key=pub_key,
        )

    def get_for_resource(self, resource: str) -> Actor:
        """Returns Actor matching resource [acct:]name@domain.

        Raises DoesNotExist if not found.
        """

        if resource.startswith("acct:"):
            resource = resource[5:]

        try:
            handle, domain = resource.split("@")
        except ValueError as e:
            raise self.model.DoesNotExist from e

        return self.get(
            instance__domain__iexact=domain,
            handle__iexact=handle,
        )


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

    # for a Local instance user
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        related_name="actor",
        on_delete=models.SET_NULL,
    )

    # blocked for all users: each user will have own block list
    blocked = models.BooleanField(default=False)

    # for Remote instances
    profile_url = models.URLField(blank=True)
    outbox_url = models.URLField(blank=True)
    inbox_url = models.URLField(blank=True)

    # for Local instances
    private_key = models.TextField(blank=True)
    public_key = models.TextField(blank=True)

    objects = ActorQuerySet.as_manager()

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

    def __str__(self) -> str:
        """Return handle"""
        return self.handle

    def get_resource(self) -> str:
        """Returns name@domain"""
        return f"{self.handle}@{self.instance.domain}"


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
            ),
        ]
