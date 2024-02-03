from collections.abc import Callable

from django.contrib.messages import get_messages
from django.http import HttpRequest, HttpResponse
from django.template.loader import render_to_string
from django_htmx.http import HttpResponseLocation


class BaseMiddleware:
    """Base class for middleware"""

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]):
        self.get_response = get_response


class CacheControlMiddleware(BaseMiddleware):
    """Workaround for https://github.com/bigskysoftware/htmx/issues/497.

    Place after HtmxMiddleware.
    """

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """Middleware implementation."""
        response = self.get_response(request)
        if request.htmx:
            # don't override if cache explicitly set
            response.setdefault("Cache-Control", "no-store, max-age=0")
        return response


class HtmxMessagesMiddleware(BaseMiddleware):
    """Adds messages to HTMX response"""

    _hx_redirect_headers = frozenset(
        {
            "HX-Location",
            "HX-Redirect",
            "HX-Refresh",
        }
    )

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """Middleware implementation"""
        response = self.get_response(request)

        if not request.htmx:
            return response

        if set(response.headers) & self._hx_redirect_headers:
            return response

        if get_messages(request):
            response.write(
                render_to_string(
                    template_name="_messages.html",
                    context={"hx_oob": True},
                    request=request,
                )
            )

        return response


class HtmxRedirectMiddleware(BaseMiddleware):
    """If HTMX request will send HX-Location response header if HTTP redirect."""

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """Middleware implementation"""
        response = self.get_response(request)
        if request.htmx and "Location" in response:
            return HttpResponseLocation(response["Location"])
        return response
