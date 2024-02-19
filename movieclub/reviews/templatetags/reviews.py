from django import template
from django.template.context import RequestContext
from django.template.defaultfilters import urlencode
from django.urls import reverse

from movieclub.releases.models import Release
from movieclub.reviews.forms import ReviewForm

register = template.Library()


@register.inclusion_tag("reviews/_reviews.html", takes_context=True)
def review_list(context: RequestContext, release: Release) -> dict:
    """Render list of reviews and form if authenticated."""
    rv = {
        "request": context.request,
        "reviews": release.reviews.select_related("user").order_by("-created"),
    }

    if context.request.user.is_authenticated:
        rv = {
            **rv,
            "review_form": ReviewForm(),
            "review_submit_url": reverse("reviews:add_review", args=[release.pk]),
        }
    else:
        rv = {
            **rv,
            "login_url": f"{reverse('account_login')}?next={urlencode(context.request.path)}",
        }
    return rv
