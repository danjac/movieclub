from django.http import Http404, HttpRequest, JsonResponse
from django.views.decorators.http import require_GET

from movieclub.users.models import User


@require_GET
def webfinger(request: HttpRequest) -> JsonResponse:
    """Webfinger implementation for user."""

    try:
        resource = request.GET["resource"]
        if resource.startswith("acct:"):
            resource = resource[5:]

        username, domain = resource.split("@")
        if domain != request.site.domain:
            raise ValueError(f"invalid domain: {domain}")

        user = User.objects.get(is_active=True, username__iexact=username)
        handle = f"{user.username}@{request.site.domain}"

    except (KeyError, ValueError, User.DoesNotExist) as e:
        raise Http404 from e

    return JsonResponse(
        {
            "subject": f"acct:{handle}",
            "links": [
                {
                    "rel": "self",
                    "type": "application/activity+json",
                    "href": f"https://{handle}",
                },
            ],
        }
    )


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
