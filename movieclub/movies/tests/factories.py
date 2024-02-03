import faker

from movieclub.movies.models import CastMember, CrewMember, Movie
from movieclub.people.models import Person
from movieclub.people.tests.factories import create_person
from movieclub.tests.factories import NotSet, resolve

_faker = faker.Faker()


def acreate_movie(**kwargs) -> Movie:
    return Movie.objects.acreate(**_movie_kwargs(**kwargs))


def create_movie(**kwargs) -> Movie:
    return Movie.objects.create(**_movie_kwargs(**kwargs))


def create_cast_member(
    *,
    person: Person = NotSet,
    movie: Movie = NotSet,
    character: str = "Lead Role",
    order: int = 0,
    **kwargs,
) -> CastMember:
    return CastMember.objects.create(
        person=resolve(person, create_person),
        movie=resolve(movie, create_movie),
        character=character,
        order=order,
        **kwargs,
    )


def create_crew_member(
    *,
    person: Person = NotSet,
    movie: Movie = NotSet,
    job: str = "Director",
    **kwargs,
) -> CrewMember:
    return CrewMember.objects.create(
        person=resolve(person, create_person),
        movie=resolve(movie, create_movie),
        job=job,
        **kwargs,
    )


def _movie_kwargs(*, tmdb_id: int = NotSet, title: str = NotSet, **kwargs):
    return {
        "tmdb_id": resolve(tmdb_id, _faker.unique.numerify),
        "title": resolve(title, _faker.sentence),
        **kwargs,
    }
