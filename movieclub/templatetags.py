from __future__ import annotations

import functools
import urllib.parse
from typing import TYPE_CHECKING, Final, TypedDict

from django import template
from django.core.signing import Signer
from django.shortcuts import resolve_url
from django.template.loader import render_to_string
from django.urls import reverse

if TYPE_CHECKING:  # pragma: nocover
    from django.template.base import NodeList, Parser
    from django.template.context import RequestContext

ACCEPT_COOKIES_NAME: Final = "accept-cookies"

COVER_IMAGE_SIZES: Final = (
    (100, 150),
    (200, 300),
    (800, 800),
)


class Breadcrumb(TypedDict):
    """A breadcrumb in list"""

    text: str
    url: str | None


register = template.Library()


@register.inclusion_tag("_cookie_notice.html", takes_context=True)
def cookie_notice(context: RequestContext) -> dict:
    """Renders GDPR cookie notice. Notice should be hidden once user has clicked
    "Accept Cookies" button."""
    return {"accept_cookies": ACCEPT_COOKIES_NAME in context.request.COOKIES}


@register.simple_tag
@functools.cache
def get_cover_image_url(cover_url: str | None, width: int, height: int) -> str:
    """Returns signed cover image URL."""

    assert (
        width,
        height,
    ) in COVER_IMAGE_SIZES, f"invalid cover image size: {width}x{height}"

    if cover_url:
        return (
            reverse(
                "cover_image",
                kwargs={
                    "width": width,
                    "height": height,
                },
            )
            + "?"
            + urllib.parse.urlencode({"url": Signer().sign(cover_url)})
        )
    return ""


@register.simple_tag
@functools.cache
def get_placeholder_cover_url(width: int, height: int) -> str:
    """Return placeholder cover image URL."""
    return f"https://placehold.co/{width}x{height}"


@register.inclusion_tag("_cover_image.html")
@functools.cache
def cover_image(
    cover_url: str | None,
    width: int,
    height: int,
    title: str,
    css_class: str = "",
) -> dict:
    """Renders a cover image with proxy URL."""

    return {
        "cover_url": get_cover_image_url(cover_url, width, height),
        "placeholder": get_placeholder_cover_url(width, height),
        "title": title,
        "width": width,
        "height": height,
        "css_class": css_class,
    }


@register.simple_tag(takes_context=True)
def pagination_url(context: RequestContext, page_number: int) -> str:
    """Returns URL for next/previous page."""
    return context.request.pagination.url(page_number)


@register.inclusion_tag("_search_form.html", takes_context=True)
def search_form(
    context: RequestContext,
    placeholder: str,
    search_url: str = "",
    clear_search_url: str = "",
) -> dict:
    """Renders search form component."""
    return {
        "placeholder": placeholder,
        "search_url": search_url or context.request.path,
        "clear_search_url": clear_search_url or context.request.path,
        "request": context.request,
    }


class BreadcrumbsNode(template.Node):
    """Renders breadcrumbs."""

    def __init__(self, nodelist: NodeList):
        self.nodelist = nodelist

    def render(self, context: RequestContext) -> str:
        """Render the breadcrumbs to template"""
        with context.push():
            for node in self.nodelist:
                node.render_annotated(context)
            return render_to_string("_breadcrumbs.html", context.flatten())


@register.tag()
def breadcrumbs(parser: Parser, _) -> BreadcrumbsNode:
    """Render breadcrumbs."""
    nodelist = parser.parse(("endbreadcrumbs",))
    parser.delete_first_token()
    return BreadcrumbsNode(nodelist)


@register.simple_tag(takes_context=True)
def breadcrumb(context, text: str, urlname: str | None = None, *args, **kwargs) -> None:
    """Adds breadcrumb to list."""
    breadcrumbs = context.get("BREADCRUMBS", [])
    url = resolve_url(urlname, *args, **kwargs) if urlname else None
    breadcrumbs.append(Breadcrumb(text=text, url=url))
    context["BREADCRUMBS"] = breadcrumbs
