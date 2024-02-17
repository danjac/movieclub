import pytest

from movieclub.movies.models import Genre, Movie
from movieclub.movies.tests.factories import (
    create_cast_member,
    create_crew_member,
    create_movie,
)


class TestGenre:
    def test_str(self):
        genre = Genre(name="Action")
        assert str(genre) == "Action"


class TestMovie:
    def test_str(self):
        movie = Movie(title="John Wick")
        assert str(movie) == "John Wick"

    @pytest.mark.django_db()
    def test_search(self):
        movie = create_movie(title="John Wick")
        assert Movie.objects.search("john wick").first() == movie

    @pytest.mark.django_db()
    def test_search_empty(self):
        create_movie(title="John Wick")
        assert Movie.objects.search("").count() == 0


class TestCastMember:
    @pytest.mark.django_db()
    def test_str(self):
        member = create_cast_member()
        assert str(member) == "Lead Role"


class TestCrewMember:
    @pytest.mark.django_db()
    def test_str(self):
        member = create_crew_member()
        assert str(member) == "Director"
