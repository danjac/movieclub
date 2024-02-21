from __future__ import annotations

from django.conf import settings
from django.db import models
from model_utils.models import TimeStampedModel


class Collection(TimeStampedModel):
    """Collection model."""

    name = models.CharField(max_length=120)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="collections",
    )

    releases = models.ManyToManyField(
        "releases.Release",
        through="CollectionItem",
    )


class CollectionItem(TimeStampedModel):
    """Item in Collection."""

    collection = models.ForeignKey(
        Collection,
        on_delete=models.CASCADE,
    )
    release = models.ForeignKey(
        "releases.Release",
        on_delete=models.CASCADE,
    )
