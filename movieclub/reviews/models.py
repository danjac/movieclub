import uuid
from typing import ClassVar

from django.conf import settings
from django.db import models
from model_utils.managers import InheritanceManager
from model_utils.models import TimeStampedModel


class BaseReview(TimeStampedModel):
    """Abstract model class."""

    class ActivitypubStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        DISPATCHED = "dispatched", "Dispatched"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    actor = models.ForeignKey(
        "activitypub.Actor",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    # should be unique for actor+instance or local site
    activitypub_object_id = models.CharField(max_length=200, default=uuid.uuid4)

    activitypub_status = models.CharField(
        max_length=12,
        default=ActivitypubStatus.PENDING,
        choices=ActivitypubStatus,
    )

    url = models.URLField(blank=True)

    comment = models.TextField()

    objects = InheritanceManager()

    class Meta:
        abstract: ClassVar = True

        constraints: ClassVar = [
            models.CheckConstraint(
                check=models.Q(
                    models.Q(user__isnull=False, actor__isnull=True)
                    | models.Q(actor__isnull=False, user__isnull=True),
                ),
                name="%(app_label)s_%(class)s_actor_or_user",
            ),
            models.UniqueConstraint(
                fields=["activitypub_object_id", "user"],
                name="%(app_label)s_%(class)s_unique_local_object_id",
                condition=models.Q(user__isnull=False),
            ),
            models.UniqueConstraint(
                fields=["activitypub_object_id", "actor"],
                name="%(app_label)s_%(class)s_unique_remote_object_id",
                condition=models.Q(actor__isnull=False),
            ),
        ]

    def get_target_id(self) -> str:
        """Return HTMX target in DOM."""
        raise NotImplementedError  # pragma: no cover

    def get_delete_url(self) -> str:
        """URL to delete endpoint."""
        raise NotImplementedError  # pragma: no cover
