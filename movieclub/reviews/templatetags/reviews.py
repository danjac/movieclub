from django import template

from movieclub.releases.models import Release

register = template.Library()


@register.simple_tag
def get_latest_reviews(release: Release, limit: int) -> dict:
    """Render list of reviews."""
    return release.reviews.select_related("review", "release").order_by("-created")[
        :limit
    ]
