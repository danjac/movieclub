import http

import pytest
from django.urls import reverse, reverse_lazy

from movieclub import tmdb
from movieclub.movies.models import Movie, Review
from movieclub.movies.tests.factories import create_movie, create_review
from movieclub.tests.factories import create_batch


class TestIndex:
    url = reverse_lazy("movies:index")

    @pytest.mark.django_db()
    def test_get(self, client):
        create_batch(create_movie, 10)
        response = client.get(self.url)
        assert response.status_code == http.HTTPStatus.OK


class TestDetail:
    @pytest.mark.django_db()
    def test_get(self, client):
        movie = create_movie()
        create_batch(create_review, 3, movie=movie)
        response = client.get(movie.get_absolute_url())
        assert response.status_code == http.HTTPStatus.OK

    @pytest.mark.django_db()
    def test_get_for_user(self, client, auth_user):
        movie = create_movie()
        create_batch(create_review, 3, movie=movie)
        response = client.get(movie.get_absolute_url())
        assert response.status_code == http.HTTPStatus.OK


class TestAddReview:
    @pytest.mark.django_db()
    def test_post(self, client, auth_user):
        movie = create_movie()
        response = client.post(
            reverse("movies:add_review", args=[movie.pk]),
            {"comment": "test!"},
        )

        assert response.status_code == http.HTTPStatus.OK
        assert movie.reviews.filter(user=auth_user).count() == 1

    @pytest.mark.django_db()
    def test_post_invalid(self, client, auth_user):
        movie = create_movie()
        response = client.post(reverse("movies:add_review", args=[movie.pk]), {})

        assert response.status_code == http.HTTPStatus.OK
        assert movie.reviews.filter(user=auth_user).count() == 0


class TestEditReview:
    @pytest.mark.django_db()
    def test_get_is_owner(self, client, auth_user):
        review = create_review(user=auth_user)
        response = client.get(review.get_edit_url())
        assert response.status_code == http.HTTPStatus.OK

    @pytest.mark.django_db()
    def test_get_cancel(self, client, auth_user):
        review = create_review(user=auth_user)
        response = client.get(review.get_edit_url(), {"action": "cancel"})
        assert response.status_code == http.HTTPStatus.OK

    @pytest.mark.django_db()
    def test_get_is_not_owner(self, client, auth_user):
        review = create_review()
        response = client.get(review.get_edit_url())
        assert response.status_code == http.HTTPStatus.NOT_FOUND

    @pytest.mark.django_db()
    def test_post(self, client, auth_user):
        review = create_review(user=auth_user)
        response = client.post(
            review.get_edit_url(),
            {
                "comment": "updated comment!",
                "url": "https://example.com",
            },
        )
        assert response.status_code == http.HTTPStatus.OK

        review.refresh_from_db()
        assert review.comment == "updated comment!"
        assert review.url == "https://example.com"


class TestDeleteReview:
    @pytest.mark.django_db()
    def test_delete_is_owner(self, client, auth_user):
        review = create_review(user=auth_user)
        response = client.delete(review.get_delete_url())
        assert response.status_code == http.HTTPStatus.OK
        assert Review.objects.exists() is False

    @pytest.mark.django_db()
    def test_delete_is_not_owner(self, client, auth_user):
        review = create_review()
        response = client.delete(review.get_delete_url())
        assert response.status_code == http.HTTPStatus.OK
        assert Review.objects.exists() is True


class TestSearchTmdb:
    url = reverse_lazy("movies:search_tmdb")

    @pytest.mark.django_db()
    def test_get(self, client, mocker, auth_user):
        mocker.patch(
            "movieclub.tmdb.search_movies",
            return_value=[
                tmdb.Movie(
                    id=1000,
                    title="John Wick",
                    release_date="2014-01-01",
                )
            ],
        )

        response = client.get(self.url, {"query": "Wick"})
        assert response.status_code == http.HTTPStatus.OK


class TestAddMovie:
    tmdb_id = 245891
    url = reverse_lazy("movies:add_movie", args=[tmdb_id])
    params = {
        "title": "John Wick 4",
        "overview": "test",
        "poster": "https://example.com/poster.jpg",
    }

    @pytest.fixture()
    def mock_populate_movie(self, mocker):
        return mocker.patch("movieclub.movies.jobs.populate_movie.delay")

    @pytest.mark.django_db(transaction=True)
    def test_post_new(self, client, auth_user, mock_populate_movie):
        response = client.post(self.url, self.params)
        movie = Movie.objects.get(tmdb_id=self.tmdb_id)
        assert movie.title == "John Wick 4"
        assert response.url == movie.get_absolute_url()
        mock_populate_movie.assert_called()

    @pytest.mark.django_db(transaction=True)
    def test_post_new_missing_params(self, client, auth_user, mock_populate_movie):
        response = client.post(self.url)
        assert response.status_code == http.HTTPStatus.BAD_REQUEST
        assert Movie.objects.exists() is False
        mock_populate_movie.assert_not_called()

    @pytest.mark.django_db(transaction=True)
    def test_post_exists(self, client, auth_user, mock_populate_movie):
        movie = create_movie(tmdb_id=self.tmdb_id)
        response = client.post(self.url, self.params)
        assert response.url == movie.get_absolute_url()
        mock_populate_movie.assert_not_called()
