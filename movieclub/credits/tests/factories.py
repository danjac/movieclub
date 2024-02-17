import faker

from movieclub.credits.models import CastMember, CrewMember, Person
from movieclub.releases.models import Release
from movieclub.releases.tests.factories import create_movie
from movieclub.tests.factories import NotSet, resolve

_faker = faker.Faker()


def create_person(
    *,
    tmdb_id: int = NotSet,
    name: str = NotSet,
    gender: int = Person.Gender.MALE,
    **kwargs,
) -> Person:
    return Person.objects.create(
        tmdb_id=resolve(tmdb_id, _faker.unique.numerify),
        name=resolve(name, _faker.unique.name),
        gender=gender,
    )


def create_cast_member(
    *,
    person: Person = NotSet,
    release: Release = NotSet,
    character: str = NotSet,
    **kwargs,
):
    return CastMember.objects.create(
        person=resolve(person, create_person),
        release=resolve(release, create_movie),
        character=resolve(character, _faker.name),
        **kwargs,
    )


def create_crew_member(
    *,
    person: Person = NotSet,
    release: Release = NotSet,
    job: str = NotSet,
    **kwargs,
):
    return CrewMember.objects.create(
        person=resolve(person, create_person),
        release=resolve(release, create_movie),
        job=resolve(job, _faker.text(30)),
        **kwargs,
    )
