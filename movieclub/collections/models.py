from __future__ import annotations

from typing import ClassVar

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
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

    def __str__(self) -> str:
        """Returns name."""
        return self.name

    def get_absolute_url(self) -> str:
        """Return link to detail page."""
        return reverse(
            "collections:collection_detail",
            kwargs={
                "collection_id": self.pk,
                "slug": slugify(self.name),
            },
        )


class CollectionItem(TimeStampedModel):
    """Item in Collection."""

    collection = models.ForeignKey(
        Collection,
        on_delete=models.CASCADE,
        related_name="collection_items",
    )

    release = models.ForeignKey(
        "releases.Release",
        on_delete=models.CASCADE,
        related_name="collection_items",
    )

    class Meta:
        constraints: ClassVar = [
            models.UniqueConstraint(
                fields=["collection", "release"],
                name="%(app_label)s_%(class)s_unique_collection_item",
            )
        ]
