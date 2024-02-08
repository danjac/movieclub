from django.http import Http404, HttpRequest, JsonResponse
from django.views.decorators.http import require_GET

from movieclub.activitypub.models import Actor


@require_GET
def webfinger(request: HttpRequest) -> JsonResponse:
    """Webfinger implementation for user."""

    if resource := request.GET.get("resource"):
        try:
            actor = (
                Actor.objects.local()
                .select_related("instance")
                .get_for_resource(resource)
            )
        except Actor.DoesNotExist as e:
            raise Http404 from e

        resource = actor.get_resource()

        return JsonResponse(
            {
                "subject": f"acct:{resource}",
                "links": [
                    {
                        "rel": "self",
                        "type": "application/activity+json",
                        "href": f"https://{resource}",
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
                    "total": Actor.objects.local().count(),
                },
                "localPosts": 0,
            },
            "openRegistrations": False,
        }
    )
