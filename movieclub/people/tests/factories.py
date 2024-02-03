import faker

from movieclub.people.models import Person
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
