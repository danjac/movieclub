from django.conf import settings
from django.db import models
from model_utils.models import TimeStampedModel


class Review(TimeStampedModel):
    """Abstract model class."""

    release = models.ForeignKey(
        "releases.Release",
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="reviews",
    )

    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="replies",
    )

    url = models.URLField(blank=True)

    comment = models.TextField()

    def get_target_id(self) -> str:
        """Return HTMX target in DOM."""
        return f"review-{self.pk}"
