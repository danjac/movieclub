import pytest

from movieclub.releases.models import Genre, Release
from movieclub.releases.tests.factories import create_movie, create_tv_show


class TestGenre:
    def test_str(self):
        genre = Genre(name="Action")
        assert str(genre) == "Action"


class TestRelease:
    def test_str(self):
        movie = Release(title="John Wick")
        assert str(movie) == "John Wick"

    @pytest.mark.django_db()
    def test_movies(self):
        create_movie()
        assert Release.objects.movies().count() == 1

    @pytest.mark.django_db()
    def test_tv_shows(self):
        create_tv_show()
        assert Release.objects.tv_shows().count() == 1

    @pytest.mark.django_db()
    def test_search(self):
        movie = create_movie(title="John Wick")
        assert Release.objects.search("john wick").first() == movie

    @pytest.mark.django_db()
    def test_search_empty(self):
        create_movie(title="John Wick")
        assert Release.objects.search("").count() == 0
