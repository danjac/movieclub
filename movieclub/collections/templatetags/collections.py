from django import template
from django.db.models import Exists, OuterRef
from django.template.context import RequestContext

from movieclub.collections.models import CollectionItem
from movieclub.releases.models import Release

register = template.Library()


@register.inclusion_tag("collections/_dropdown.html", takes_context=True)
def collection_dropdown(context: RequestContext, release: Release) -> dict:
    """Collection selector component."""
    if context.request.user.is_authenticated:
        collections = context.request.user.collections.annotate(
            is_added=Exists(
                CollectionItem.objects.filter(
                    collection=OuterRef("pk"), release=release
                )
            )
        ).order_by("name")

        return {"collections": collections, "release": release}
    return {}
