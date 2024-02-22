import faker

from movieclub.releases.models import Genre, Release
from movieclub.tests.factories import NotSet, resolve

_faker = faker.Faker()


def create_movie(
    tmdb_id: int = NotSet,
    title: str = NotSet,
    **kwargs,
) -> Release:
    return Release.objects.create(
        tmdb_id=resolve(tmdb_id, _faker.unique.numerify),
        category=Release.Category.MOVIE,
        title=resolve(title, _faker.sentence),
        **kwargs,
    )


def create_tv_show(tmdb_id: int = NotSet, title: str = NotSet, **kwargs) -> Release:
    return Release.objects.create(
        tmdb_id=resolve(tmdb_id, _faker.unique.numerify),
        category=Release.Category.TV_SHOW,
        title=resolve(title, _faker.sentence),
        **kwargs,
    )


def create_genre(tmdb_id: int = NotSet, name: str = NotSet, **kwargs) -> Genre:
    return Genre.objects.create(
        tmdb_id=resolve(tmdb_id, _faker.unique.numerify),
        name=resolve(name, _faker.unique.word()),
        **kwargs,
    )
