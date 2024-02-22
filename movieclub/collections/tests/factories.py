import faker

from movieclub.collections.models import Collection, CollectionItem
from movieclub.releases.models import Release
from movieclub.releases.tests.factories import create_movie
from movieclub.tests.factories import NotSet, resolve
from movieclub.users.models import User
from movieclub.users.tests.factories import create_user

_faker = faker.Faker()


def create_collection(
    *,
    name: str = NotSet,
    user: User = NotSet,
    **kwargs,
) -> Collection:
    return Collection.objects.create(
        name=resolve(name, _faker.text(60)),
        user=resolve(user, create_user),
        **kwargs,
    )


def create_collection_item(
    *,
    collection: Collection = NotSet,
    release: Release = NotSet,
    **kwargs,
):
    return CollectionItem.objects.create(
        collection=resolve(collection, create_collection),
        release=resolve(release, create_movie),
        **kwargs,
    )
