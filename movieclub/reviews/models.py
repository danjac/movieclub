from django.conf import settings
from django.db import models
from model_utils.models import TimeStampedModel


class BaseReview(TimeStampedModel):
    """Abstract model class."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    url = models.URLField(blank=True)

    comment = models.TextField()

    class Meta:
        abstract = True

    def get_target_id(self) -> str:
        """Return HTMX target in DOM."""
        raise NotImplementedError  # pragma: no cover

    def get_delete_url(self) -> str:
        """URL to delete endpoint."""
        raise NotImplementedError  # pragma: no cover
