from django.contrib import messages
from django.db.models import Exists, OuterRef, Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_safe

from movieclub.blogathons.models import Blogathon, Entry
from movieclub.decorators import require_auth, require_form_methods
from movieclub.htmx import render_htmx
from movieclub.pagination import render_pagination
from movieclub.users.forms import UserDetailsForm
from movieclub.users.models import User


@require_safe
def user_detail(request: HttpRequest, username: str) -> HttpResponse:
    """Return user details"""

    user = _get_user_or_404(username)

    return render(
        request,
        "users/detail.html",
        {
            "current_user": user,
            "is_current_user": user == request.user,
            "links": user.links.order_by("title"),
        },
    )


@require_form_methods
@require_auth
def edit_user_details(request: HttpRequest) -> HttpResponse:
    """Edit user details"""
    if request.method == "POST":
        form = UserDetailsForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your details have been updated")
    else:
        form = UserDetailsForm(instance=request.user)
    return render_htmx(
        request,
        "users/user_form.html",
        {"form": form},
        partial="form",
        target="user-form",
    )


@require_safe
def user_reviews(request: HttpRequest, username: str) -> HttpResponse:
    """Reviews submitted by the user"""

    user = _get_user_or_404(username)

    return render_pagination(
        request,
        user.reviews.select_related(
            "parent",
            "parent__user",
            "release",
        ).order_by("-created"),
        "users/reviews.html",
        {
            "current_user": user,
        },
    )


@require_safe
def user_blogathons(request: HttpRequest, username: str) -> HttpResponse:
    """Blogathons organized or contributed to by this user."""

    user = _get_user_or_404(username)

    return render_pagination(
        request,
        Blogathon.objects.annotate(
            has_entries=Exists(
                Entry.objects.filter(
                    participant=user,
                    blogathon=OuterRef("pk"),
                )
            )
        )
        .filter(Q(organizer=user) | Q(has_entries=True))
        .order_by("-created"),
        "users/blogathons.html",
        {
            "current_user": user,
        },
    )


@require_safe
def user_collections(request: HttpRequest, username: str) -> HttpResponse:
    """Collections belonging to this user."""

    user = _get_user_or_404(username)

    return render_pagination(
        request,
        user.collections.order_by("-created"),
        "users/blogathons.html",
        {
            "current_user": user,
        },
    )


def _get_user_or_404(username: str) -> User:
    return get_object_or_404(User, username__iexact=username, is_active=True)
