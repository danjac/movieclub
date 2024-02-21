import http

import pytest
from django.urls import reverse_lazy

from movieclub import tmdb
from movieclub.releases.models import Release
from movieclub.releases.tests.factories import (
    create_genre,
    create_movie,
    create_tv_show,
)
from movieclub.tests.factories import create_batch


class TestMovieList:
    url = reverse_lazy("releases:movie_list")

    @pytest.mark.django_db()
    def test_get(self, client):
        create_batch(create_movie, 10)
        response = client.get(self.url)
        assert response.status_code == http.HTTPStatus.OK

    @pytest.mark.django_db()
    def test_get_search(self, client):
        movie = create_movie(title="Jaws")
        response = client.get(self.url, {"query": "jaws"})
        assert response.status_code == http.HTTPStatus.OK
        assert movie in response.context["page_obj"].object_list


class TestTVShowList:
    url = reverse_lazy("releases:tv_show_list")

    @pytest.mark.django_db()
    def test_get(self, client):
        create_batch(create_movie, 10)
        response = client.get(self.url)
        assert response.status_code == http.HTTPStatus.OK

    @pytest.mark.django_db()
    def test_get_search(self, client):
        movie = create_tv_show(title="Columbo")
        response = client.get(self.url, {"query": "columbo"})
        assert response.status_code == http.HTTPStatus.OK
        assert movie in response.context["page_obj"].object_list


class TestGenreDetail:
    @pytest.fixture()
    def genre(self):
        return create_genre()

    @pytest.mark.django_db()
    def test_get(self, client, genre):
        for movie in create_batch(create_movie, 10):
            genre.movies.add(movie)
        response = client.get(genre.get_absolute_url())
        assert response.status_code == http.HTTPStatus.OK

    @pytest.mark.django_db()
    def test_get_search(self, client, genre):
        movie = create_movie(title="Jaws")
        genre.movies.add(movie)
        response = client.get(genre.get_absolute_url(), {"query": "jaws"})
        assert response.status_code == http.HTTPStatus.OK
        assert movie in response.context["page_obj"].object_list


class TestMovieDetail:
    @pytest.mark.django_db()
    def test_get(self, client):
        movie = create_movie()
        response = client.get(movie.get_absolute_url())
        assert response.status_code == http.HTTPStatus.OK

    @pytest.mark.django_db()
    def test_get_for_user(self, client, auth_user):
        movie = create_movie()
        response = client.get(movie.get_absolute_url())
        assert response.status_code == http.HTTPStatus.OK


class TestTVShowDetail:
    @pytest.mark.django_db()
    def test_get(self, client):
        movie = create_movie()
        response = client.get(movie.get_absolute_url())
        assert response.status_code == http.HTTPStatus.OK

    @pytest.mark.django_db()
    def test_get_for_user(self, client, auth_user):
        tv_show = create_tv_show()
        response = client.get(tv_show.get_absolute_url())
        assert response.status_code == http.HTTPStatus.OK


class TestSearchTmdbMovies:
    url = reverse_lazy("releases:search_tmdb_movies")

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


class TestSearchTmdbTVShows:
    url = reverse_lazy("releases:search_tmdb_tv_shows")

    @pytest.mark.django_db()
    def test_get(self, client, mocker, auth_user):
        mocker.patch(
            "movieclub.tmdb.search_tv_shows",
            return_value=[
                tmdb.TVShow(
                    id=1000,
                    name="Poker Face",
                    first_air_date="2023-01-01",
                )
            ],
        )

        response = client.get(self.url, {"query": "Poker Face"})
        assert response.status_code == http.HTTPStatus.OK


class TestAddMovie:
    tmdb_id = 245891
    url = reverse_lazy("releases:add_movie", args=[tmdb_id])

    @pytest.mark.django_db()
    def test_post_new(self, client, auth_user, mocker):
        movie = create_movie(tmdb_id=self.tmdb_id)

        mock_qs = mocker.Mock()
        mock_qs.get.side_effect = Release.DoesNotExist

        mocker.patch(
            "movieclub.releases.models.Release.objects.movies",
            return_value=mock_qs,
        )

        mocker.patch(
            "movieclub.releases.views.populate_movie",
            return_value=movie,
        )

        response = client.post(self.url)
        assert response.url == movie.get_absolute_url()

    @pytest.mark.django_db()
    def test_post_exists(self, client, auth_user):
        movie = create_movie(tmdb_id=self.tmdb_id)
        response = client.post(self.url)
        assert response.url == movie.get_absolute_url()
        assert Release.objects.movies().count() == 1


class TestAddTVShow:
    tmdb_id = 245891
    url = reverse_lazy("releases:add_tv_show", args=[tmdb_id])

    @pytest.mark.django_db()
    def test_post_new(self, client, auth_user, mocker):
        tv_show = create_tv_show(tmdb_id=self.tmdb_id)

        mock_qs = mocker.Mock()
        mock_qs.get.side_effect = Release.DoesNotExist

        mocker.patch(
            "movieclub.releases.models.Release.objects.tv_shows",
            return_value=mock_qs,
        )

        mocker.patch(
            "movieclub.releases.views.populate_tv_show",
            return_value=tv_show,
        )

        response = client.post(self.url)
        assert response.url == tv_show.get_absolute_url()

    @pytest.mark.django_db()
    def test_post_exists(self, client, auth_user):
        tv_show = create_tv_show(tmdb_id=self.tmdb_id)
        response = client.post(self.url)
        assert response.url == tv_show.get_absolute_url()
        assert Release.objects.tv_shows().count() == 1
