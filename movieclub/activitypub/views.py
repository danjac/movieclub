from django.http import Http404, HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.http import require_POST, require_safe

from movieclub.activitypub.signature import InvalidSignatureError, verify_signature
from movieclub.client import get_client
from movieclub.http import HttpResponseUnauthorized
from movieclub.users.models import User


@require_safe
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


@require_safe
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


@require_POST
def inbox(request: HttpRequest, username: str) -> JsonResponse:
    """
    1. Check for "Signature" header.
    2. Fetch JSON from the keyId value.
    3. In JSON publicKey.pubkeyPrem get public key.
    4. Build and compare the strings.
    5. Verify the signature, digest etc. Return 401 if bad sig.

    Parse message:
        - Follow Activity: generatate a remote->local Follow object
        and notify user.
    """

    try:
        verify_signature(request, get_client())
    except InvalidSignatureError as e:
        raise HttpResponseUnauthorized from e

    return HttpResponse()
