from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.decorators.http import require_POST, require_safe
from django_htmx.http import reswap, retarget

from movieclub.decorators import require_auth, require_DELETE, require_form_methods
from movieclub.releases.models import Release
from movieclub.reviews.forms import ReviewForm
from movieclub.reviews.models import Review


@require_POST
@require_auth
def add_review(request: HttpRequest, release_id: int) -> HttpResponse:
    """Add new review"""
    release = get_object_or_404(Release, pk=release_id)
    form = ReviewForm(request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.user = request.user
        review.release = release
        review.save()

        messages.success(request, "Your review has been posted, thanks!")
        return _render_new_review(request, review)

    return _render_review_form(request, form)


@require_form_methods
@require_auth
def reply_to_review(request: HttpRequest, parent_id: int) -> HttpResponse:
    """Add new review in reply to another review."""
    parent = get_object_or_404(
        Review.objects.select_related("user", "release"), pk=parent_id
    )
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.parent = parent
            review.release = parent.release
            review.save()

            messages.success(request, "Your reply has been posted, thanks!")
            # TBD: notify parent user

            return _render_new_review(request, review)
    else:
        form = ReviewForm()

    return _render_review_form(request, form, {"parent": parent})


@require_form_methods
@require_auth
def edit_review(request: HttpRequest, review_id: int) -> HttpResponse:
    """Update review."""
    review = get_object_or_404(
        Review.objects.select_related("release", "parent", "user", "parent__user"),
        user=request.user,
        pk=review_id,
    )

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, "Your review has been updated")
            target = f"#{review.get_target_id()}"
            return reswap(
                retarget(
                    _render_current_review(
                        request,
                        review,
                    ),
                    target,
                ),
                f"outerHTML show:{target}:top",
            )

    else:
        form = ReviewForm(instance=review)

    return _render_review_form(request, form, {"review": review})


@require_safe
def cancel_review(request: HttpRequest, review_id: int) -> HttpResponse:
    """Cancel form edit or reply action."""
    review = get_object_or_404(
        Review.objects.select_related(
            "parent",
            "parent__user",
            "release",
            "user",
        ),
        pk=review_id,
    )
    return _render_current_review(request, review)


@require_DELETE
@require_auth
def delete_review(request: HttpRequest, review_id: int) -> HttpResponse:
    """Delete a review."""
    review = get_object_or_404(Review, user=request.user, pk=review_id)
    review.delete()
    messages.info(request, "Your review has been deleted")
    return HttpResponse()


def _render_review(
    request: HttpRequest, review: Review, extra_context: dict | None = None
) -> HttpResponse:
    return render(
        request,
        "reviews/_reviews.html#review",
        {
            "review": review,
            **(extra_context or {}),
        },
    )


def _render_review_form(
    request: HttpRequest, form: ReviewForm, extra_context: dict | None = None
) -> HttpResponse:
    return render(
        request,
        "reviews/_reviews.html#review_form",
        {
            "review_form": form,
            "review_submit_url": request.path,
            **(extra_context or {}),
        },
    )


def _render_new_review(request: HttpRequest, review: Review) -> HttpResponse:
    return retarget(
        reswap(
            _render_review_form_to_response(
                request,
                _render_review(request, review),
                release=review.release,
            ),
            f"afterbegin show:#{review.get_target_id()}:top",
        ),
        "#reviews",
    )


def _render_current_review(request: HttpRequest, review: Review) -> HttpResponse:
    return _render_review_form_to_response(
        request,
        _render_review(request, review),
        release=review.release,
    )


def _render_review_form_to_response(
    request: HttpRequest,
    response: HttpResponse,
    *,
    release: Release,
) -> HttpResponse:
    response.write(
        render_to_string(
            template_name="reviews/_reviews.html#review_form",
            context={
                "hx_oob": True,
                "review_form": ReviewForm(),
                "review_submit_url": reverse("reviews:add_review", args=[release.pk]),
            },
            request=request,
        )
    )
    return response
