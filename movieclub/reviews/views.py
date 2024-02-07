from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django_htmx.http import reswap, retarget

from movieclub.reviews.forms import BaseReviewForm
from movieclub.reviews.models import AbstractBaseReview


def render_review_edit_form(
    request: HttpRequest,
    review: AbstractBaseReview,
    form: BaseReviewForm,
    *,
    is_success: bool = False,
) -> HttpResponse:
    """Render edit form or updated review."""
    context = {
        "review": review,
        "review_submit_url": request.path,
    }
    if is_success:
        return retarget(
            reswap(
                render(request, "reviews/_review.html", context),
                "innerHTML",
            ),
            f"#{review.get_target_id()}",
        )

    if request.GET.get("action") == "cancel":
        return render(request, "reviews/_review.html", context)

    return render(
        request,
        "reviews/_review_form.html",
        {
            **context,
            "review_form": form,
        },
    )


def render_review_create_form(
    request: HttpRequest,
    form: BaseReviewForm,
    review: AbstractBaseReview | None = None,
) -> HttpResponse:
    """Renders new review and form as needed."""
    if review is not None:
        return retarget(
            reswap(
                render(
                    request,
                    "reviews/_review.html",
                    {
                        "review": review,
                        "review_form": form,
                        "review_submit_url": request.path,
                        "new_review": True,
                    },
                ),
                "afterbegin",
            ),
            "#reviews",
        )

    return render(
        request,
        "reviews/_review_form.html",
        {
            "review_form": form,
            "review_submit_url": request.path,
        },
    )
