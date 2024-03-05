from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_safe

from movieclub.decorators import require_auth, require_form_methods
from movieclub.htmx import render_htmx
from movieclub.users.forms import UserDetailsForm
from movieclub.users.models import User


@require_safe
def user_detail(request: HttpRequest, username: str) -> HttpResponse:
    """Return user details"""

    user = get_object_or_404(User, is_active=True, username__iexact=username)

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
