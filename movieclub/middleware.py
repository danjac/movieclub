from collections.abc import Callable
from urllib.parse import urlencode

from django.contrib.messages import get_messages
from django.http import HttpRequest, HttpResponse
from django.template.loader import render_to_string
from django.utils.encoding import force_str
from django.utils.functional import cached_property
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


class PaginationMiddleware(BaseMiddleware):
    """Adds `Pagination` instance as `request.pagination`."""

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """Middleware implementation."""
        request.pagination = Pagination(request)
        return self.get_response(request)


class SearchMiddleware(BaseMiddleware):
    """Adds `Search` instance as `request.search`."""

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """Middleware implementation."""
        request.search = Search(request)
        return self.get_response(request)


class Pagination:
    """Handles pagination parameters in request."""

    param: str = "page"

    def __init__(self, request: HttpRequest):
        self.request = request

    def __str__(self) -> str:
        """Returns current page."""
        return self.current

    @cached_property
    def current(self) -> str:
        """Returns current page number from query string."""
        return self.request.GET.get(self.param, "")

    def url(self, page_number: int) -> str:
        """Inserts the page query string parameter with the provided page number into
        the current query string.

        Preserves the original request path and any other query string parameters.
        """
        qs = self.request.GET.copy()
        qs[self.param] = page_number
        return f"{self.request.path}?{qs.urlencode()}"


class Search:
    """Handles search parameters in request."""

    param: str = "query"

    def __init__(self, request: HttpRequest):
        self.request = request

    def __str__(self) -> str:
        """Returns search query value."""
        return self.value

    def __bool__(self) -> bool:
        """Returns `True` if search in query and has a non-empty value."""
        return bool(self.value)

    @cached_property
    def value(self) -> str:
        """Returns the search query value, if any."""
        return force_str(self.request.GET.get(self.param, "")).strip()

    @cached_property
    def qs(self) -> str:
        """Returns encoded query string value, if any."""
        return urlencode({self.param: self.value}) if self.value else ""
