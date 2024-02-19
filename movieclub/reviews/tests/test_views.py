import http

import pytest
from django.urls import reverse

from movieclub.releases.tests.factories import create_movie
from movieclub.reviews.models import Review
from movieclub.reviews.tests.factories import create_review


@pytest.fixture()
def review(auth_user):
    return create_review(user=auth_user)


class TestAddReview:
    @pytest.mark.django_db()
    def test_post(self, client, auth_user):
        movie = create_movie()
        response = client.post(
            reverse("reviews:add_review", args=[movie.pk]),
            {"comment": "test"},
        )
        assert response.status_code == http.HTTPStatus.OK
        review = Review.objects.get()
        assert review.release == movie
        assert review.user == auth_user

    @pytest.mark.django_db()
    def test_post_invalid(self, client, auth_user):
        movie = create_movie()
        response = client.post(
            reverse("reviews:add_review", args=[movie.pk]),
            {"comment": ""},
        )

        assert response.status_code == http.HTTPStatus.OK
        assert Review.objects.count() == 0


class TestReviewDetail:
    @pytest.mark.django_db()
    def test_get(self, client, review):
        response = client.get(
            reverse("reviews:review_detail", args=[review.pk]),
        )
        assert response.status_code == http.HTTPStatus.OK


class TestEditReview:
    @pytest.mark.django_db()
    def test_get(self, client, review):
        response = client.get(
            reverse("reviews:edit_review", args=[review.pk]),
        )
        assert response.status_code == http.HTTPStatus.OK

    @pytest.mark.django_db()
    def test_post(self, client, review):
        response = client.post(
            reverse("reviews:edit_review", args=[review.pk]),
            {"comment": "test"},
        )
        assert response.status_code == http.HTTPStatus.OK
        review.refresh_from_db()
        assert review.comment == "test"


class TestDeleteReview:
    @pytest.mark.django_db()
    def test_get(self, client, review):
        response = client.delete(
            reverse("reviews:delete_review", args=[review.pk]),
        )
        assert response.status_code == http.HTTPStatus.OK
        assert Review.objects.count() == 0
