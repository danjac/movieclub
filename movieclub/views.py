from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_safe


@require_safe
def landing_page(request: HttpRequest) -> HttpResponse:
    """Renders the landing page."""
    return render(request, "index.html")
