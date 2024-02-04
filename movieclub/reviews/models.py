from django.conf import settings
from django.db import models


class AbstractBaseReview(models.Model):
    """Abstract model class."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    url = models.URLField(blank=True)

    comment = models.TextField()

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        """Return review ID"""
        return f"Review: {self.pk}"
