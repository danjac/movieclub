import http

import pytest
from django.urls import reverse

from movieclub.releases.tests.factories import create_movie
from movieclub.reviews.models import Review
from movieclub.reviews.tests.factories import create_review


@pytest.fixture()
def review(auth_user):
    return create_review(user=auth_user)


@pytest.fixture()
def movie():
    return create_movie()


class TestAddReview:
    @pytest.fixture()
    def url(self, movie):
        return reverse("reviews:add_review", args=[movie.pk])

    @pytest.mark.django_db()
    def test_post(self, client, auth_user, movie, url):
        response = client.post(
            url,
            {"comment": "test"},
            HTTP_HX_REQUEST="true",
        )
        assert response.status_code == http.HTTPStatus.OK
        review = Review.objects.get()
        assert review.release == movie
        assert review.user == auth_user

    @pytest.mark.django_db()
    def test_post_invalid(self, client, auth_user, url):
        response = client.post(
            url,
            {"comment": ""},
            HTTP_HX_REQUEST="true",
        )

        assert response.status_code == http.HTTPStatus.OK
        assert Review.objects.count() == 0


class TestEditReview:
    @pytest.fixture()
    def url(self, review):
        return reverse("reviews:edit_review", args=[review.pk])

    @pytest.fixture()
    def target(self, review):
        return review.get_target_id()

    @pytest.mark.django_db()
    def test_get(self, client, review, url, target):
        response = client.get(
            url,
            HTTP_HX_REQUEST="true",
            HTTP_HX_TARGET=target,
        )
        assert response.status_code == http.HTTPStatus.OK

    @pytest.mark.django_db()
    def test_post(self, client, review, url, target):
        response = client.post(
            url,
            {
                "comment": "test",
            },
            HTTP_HX_REQUEST="true",
            HTTP_HX_TARGET=target,
        )
        assert response.status_code == http.HTTPStatus.OK
        review.refresh_from_db()
        assert review.comment == "test"

    @pytest.mark.django_db()
    def test_post_cancel(self, client, review, url, target):
        response = client.post(
            url,
            {
                "comment": "test",
                "action": "cancel",
            },
            HTTP_HX_REQUEST="true",
            HTTP_HX_TARGET=target,
        )
        assert response.status_code == http.HTTPStatus.OK
        review.refresh_from_db()
        assert review.comment != "test"


class TestDeleteReview:
    @pytest.mark.django_db()
    def test_get(self, client, review):
        response = client.delete(
            reverse("reviews:delete_review", args=[review.pk]),
        )
        assert response.status_code == http.HTTPStatus.OK
        assert Review.objects.count() == 0
