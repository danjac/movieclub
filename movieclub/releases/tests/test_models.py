import pytest

from movieclub.releases.models import Genre, Release
from movieclub.releases.tests.factories import create_movie


class TestGenre:
    def test_str(self):
        genre = Genre(name="Action")
        assert str(genre) == "Action"


class TestMovie:
    def test_str(self):
        movie = Release(title="John Wick")
        assert str(movie) == "John Wick"

    @pytest.mark.django_db()
    def test_search(self):
        movie = create_movie(title="John Wick")
        assert Release.objects.search("john wick").first() == movie

    @pytest.mark.django_db()
    def test_search_empty(self):
        create_movie(title="John Wick")
        assert Release.objects.search("").count() == 0
