from movieclub.movies.models import Genre, Movie


class TestGenre:
    def test_str(self):
        genre = Genre(name="Action")
        assert str(genre) == "Action"


class TestMovie:
    def test_str(self):
        movie = Movie(title="John Wick")
        assert str(movie) == "John Wick"
