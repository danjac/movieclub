from typing import ClassVar

from django.conf import settings
from django.core import validators
from django.db import models
from django.urls import reverse
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

    score = models.FloatField(
        default=0,
        validators=(
            validators.MinValueValidator(0),
            validators.MaxValueValidator(5.0),
        ),
    )

    comment = models.TextField()

    class Meta:
        constraints: ClassVar = [
            models.CheckConstraint(
                check=models.Q(score__range=(0, 5.0)),
                name="%(app_label)s_%(class)s_score_in_range",
            ),
            models.UniqueConstraint(
                fields=["user", "release"], name="%(app_label)s_%(class)s_unique_review"
            ),
        ]

    def get_absolute_url(self) -> str:
        """Return review detail."""
        return reverse("reviews:review_detail", kwargs={"review_id": self.pk})
