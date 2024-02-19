import datetime
import io

import httpx
from django.core.signing import BadSignature, Signer
from django.http import FileResponse, Http404, HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.cache import cache_control, cache_page
from django.views.decorators.http import require_POST, require_safe
from PIL import Image

from movieclub.client import get_client
from movieclub.template import ACCEPT_COOKIES_NAME, COVER_IMAGE_SIZES


@require_safe
def landing_page(request: HttpRequest) -> HttpResponse:
    """Renders the landing page."""
    return render(request, "index.html")


@require_POST
def accept_cookies(_) -> HttpResponse:
    """Handles "accept" action on GDPR cookie banner."""
    response = HttpResponse()
    response.set_cookie(
        ACCEPT_COOKIES_NAME,
        value="true",
        expires=timezone.now() + datetime.timedelta(days=365),
        secure=True,
        httponly=True,
        samesite="Lax",
    )

    return response


@require_safe
@cache_control(max_age=60 * 60 * 24, immutable=True)
@cache_page(60 * 60)
def cover_image(request: HttpRequest, width: int, height=int) -> FileResponse:
    """Proxies a cover image from remote source.

    URL should be signed, so we can verify the request comes from this site.
    """

    # only specific image sizes permitted
    if (width, height) not in COVER_IMAGE_SIZES:
        raise Http404

    try:
        cover_url = Signer().unsign(request.GET["url"])

        response = get_client().get(cover_url)
        response.raise_for_status()

        image = Image.open(io.BytesIO(response.content)).resize(
            (width, height),
            Image.Resampling.LANCZOS,
        )

        output = io.BytesIO()
        image.save(output, format="webp", optimize=True, quality=90)
        output.seek(0)

        return FileResponse(output, content_type="image/webp")

    except (KeyError, OSError, httpx.HTTPError, BadSignature) as e:
        raise Http404 from e
