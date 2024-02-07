from django.http import Http404, HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET

from movieclub.users.models import User


@require_GET
def webfinger(request: HttpRequest) -> JsonResponse:
    """Webfinger implementation for user."""
    if (resource := request.GET.get("resource")) and resource.startswith("acct:"):
        user = get_object_or_404(
            User,
            is_active=True,
            username__iexact=resource[5:],
        )

        return JsonResponse(
            {
                "subject": f"acct:{user.username}",
                "links": [
                    {
                        "rel": "self",
                        "type": "application/activity+json",
                        "href": f"https://{request.site.domain}@{user.username}",
                    },
                ],
            }
        )

    raise Http404


@require_GET
def nodeinfo(request: HttpRequest) -> JsonResponse:
    """Implements NodeInfo."""

    return JsonResponse(
        {
            "version": "2.0",
            "software": {"name": "movieclub", "version": "0.0.1"},
            "protocols": ["activitypub"],
            "usage": {
                "users": {
                    "total": User.objects.filter(is_active=True).count(),
                },
                "localPosts": 0,
            },
            "openRegistrations": False,
        }
    )
