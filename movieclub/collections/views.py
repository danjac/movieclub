import contextlib

from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.html import format_html
from django.views.decorators.http import require_POST, require_safe

from movieclub.collections.forms import CollectionForm
from movieclub.collections.models import Collection, CollectionItem
from movieclub.decorators import require_auth, require_DELETE, require_form_methods
from movieclub.htmx import render_htmx
from movieclub.pagination import render_pagination
from movieclub.releases.models import Release


@require_safe
def collection_list(request: HttpRequest) -> HttpResponse:
    """Index list of collections."""
    return render_pagination(
        request,
        Collection.objects.order_by("-created").select_related("user"),
        "collections/index.html",
    )


@require_safe
def collection_detail(
    request: HttpRequest, collection_id: int, slug: str
) -> HttpResponse:
    """Render collection details."""

    collection = get_object_or_404(Collection, pk=collection_id)

    return render_pagination(
        request,
        collection.collection_items.order_by("-created").select_related("release"),
        "collections/detail.html",
        {
            "collection": collection,
        },
    )


@require_form_methods
@require_auth
def add_collection(request: HttpRequest) -> HttpResponse:
    """Add new collection."""
    if request.method == "POST":
        form = CollectionForm(request.POST)
        if form.is_valid():
            collection = form.save(commit=False)
            collection.user = request.user
            collection.save()
            messages.success(request, "Your collection has been added")
            return redirect("collections:collection_list")
    else:
        form = CollectionForm()

    return render_htmx(
        request,
        "collections/form.html",
        {"form": form},
        partial=form,
        target="collection-form",
    )


@require_form_methods
@require_auth
def edit_collection(request: HttpRequest, collection_id: int) -> HttpResponse:
    """Add new collection."""
    collection = get_object_or_404(Collection, user=request.user, pk=collection_id)

    if request.method == "POST":
        form = CollectionForm(request.POST, instance=collection)
        if form.is_valid():
            collection = form.save()
            messages.success(request, "Your collection has been updated")
            return redirect(collection)
    else:
        form = CollectionForm(instance=collection)

    return render(
        request,
        "collections/form.html",
        {
            "form": form,
            "collection": collection,
        },
    )


@require_POST
@require_auth
def add_release_to_collection(
    request: HttpRequest, collection_id: int, release_id: int
) -> HttpResponse:
    """Add a release."""
    collection = get_object_or_404(Collection, user=request.user, pk=collection_id)
    release = get_object_or_404(Release, pk=release_id)

    with contextlib.suppress(IntegrityError):
        CollectionItem.objects.create(collection=collection, release=release)

    return HttpResponse(
        format_html(
            '<input type="checkbox" hx-delete="{remove_url}" hx-swap="outerHTML" hx-target="this">',
            remove_url=reverse(
                "collections:remove_release_from_collection",
                args=[collection_id, release_id],
            ),
        )
    )


@require_DELETE
@require_auth
def remove_release_from_collection(
    request: HttpRequest, collection_id: int, release_id: int
) -> HttpResponse:
    """Add a release."""
    CollectionItem.objects.filter(
        collection__user=request.user,
        collection_id=collection_id,
        release_id=release_id,
    ).delete()

    return HttpResponse(
        format_html(
            '<input type="checkbox" hx-post="{add_url}" hx-swap="outerHTML" hx-target="this">',
            add_url=reverse(
                "collections:add_release_to_collection",
                args=[collection_id, release_id],
            ),
        )
    )
