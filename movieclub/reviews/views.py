from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.decorators.http import require_POST
from django_htmx.http import reswap, retarget

from movieclub.decorators import require_auth, require_DELETE, require_form_methods
from movieclub.htmx import render_htmx
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

        return retarget(
            reswap(
                _render_review_form_to_response(
                    request,
                    _render_review(request, review),
                    release=release,
                ),
                f"afterbegin show:#review-{review.pk}:top",  # type: ignore[arg-type]
            ),
            "#reviews",
        )
    return _render_review_form(request, form)


@require_form_methods
@require_auth
def edit_review(request: HttpRequest, review_id: int) -> HttpResponse:
    """Update review."""
    review = get_object_or_404(
        Review.objects.select_related("release"),
        user=request.user,
        pk=review_id,
    )

    form = None
    is_valid = False

    if request.method == "POST":
        if request.POST.get("action") != "cancel":
            form = ReviewForm(request.POST, instance=review)
            if is_valid := form.is_valid():
                form.save()
                messages.success(request, "Your review has been updated")

    else:
        form = ReviewForm(instance=review)

    if is_valid or form is None:
        return _render_review_form_to_response(
            request,
            reswap(
                retarget(
                    _render_review(request, review),
                    f"#review-{review.pk}",
                ),
                f"outerHTML show:#review-{review.pk}:top",  # type: ignore[arg-type]
            ),
            release=review.release,
        )

    return _render_review_form(request, form, {"review": review})


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
    return render_htmx(
        request,
        "reviews/_reviews.html",
        {
            "review": review,
            **(extra_context or {}),
        },
        partial="review",
    )


def _render_review_form(
    request: HttpRequest, form: ReviewForm, extra_context: dict | None = None
) -> HttpResponse:
    return render_htmx(
        request,
        "reviews/_reviews.html",
        {
            "review_form": form,
            "review_submit_url": request.path,
            **(extra_context or {}),
        },
        partial="review_form",
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
