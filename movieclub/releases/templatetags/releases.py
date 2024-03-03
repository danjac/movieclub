from django import template
from django.db.models import QuerySet

from movieclub.releases.models import Release

register = template.Library()


@register.simple_tag
def get_latest_releases(limit: int) -> QuerySet[Release]:
    """Returns latest movies or TV shows added to database."""

    return Release.objects.order_by("-pk")[:limit]


@register.simple_tag
def get_random_release() -> Release:
    """Returns a release at random."""
    return Release.objects.order_by("?").first()
