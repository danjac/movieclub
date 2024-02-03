import faker

from movieclub.movies.models import Movie
from movieclub.tests.factories import NotSet, resolve

_faker = faker.Faker()


def acreate_movie(**kwargs) -> Movie:
    return Movie.objects.acreate(**_movie_kwargs(**kwargs))


def create_movie(**kwargs) -> Movie:
    return Movie.objects.create(**_movie_kwargs(**kwargs))


def _movie_kwargs(*, tmdb_id: int = NotSet, title: str = NotSet, **kwargs):
    return {
        "tmdb_id": resolve(tmdb_id, _faker.unique.numerify),
        "title": resolve(title, _faker.sentence),
        **kwargs,
    }
