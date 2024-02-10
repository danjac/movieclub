import faker

from movieclub.movies.models import CastMember, CrewMember, Movie, Review
from movieclub.people.models import Person
from movieclub.people.tests.factories import create_person
from movieclub.tests.factories import NotSet, resolve
from movieclub.users.models import User
from movieclub.users.tests.factories import create_user

_faker = faker.Faker()


def create_movie(tmdb_id: int = NotSet, title: str = NotSet, **kwargs) -> Movie:
    return Movie.objects.create(
        tmdb_id=resolve(tmdb_id, _faker.unique.numerify),
        title=resolve(title, _faker.sentence),
        **kwargs,
    )


def create_review(
    *,
    movie: Movie = NotSet,
    user: User = NotSet,
    comment: str = NotSet,
    **kwargs,
) -> Review:
    return Review.objects.create(
        movie=resolve(movie, create_movie),
        user=resolve(user, create_user),
        comment=resolve(comment, _faker.text(200)),
    )


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
