import pytest

from movieclub.movies.models import Genre, Movie
from movieclub.movies.tests.factories import create_cast_member, create_crew_member


class TestGenre:
    def test_str(self):
        genre = Genre(name="Action")
        assert str(genre) == "Action"


class TestMovie:
    def test_str(self):
        movie = Movie(title="John Wick")
        assert str(movie) == "John Wick"


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
