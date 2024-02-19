import faker

from movieclub.releases.models import Release
from movieclub.releases.tests.factories import create_movie
from movieclub.reviews.models import Review
from movieclub.tests.factories import NotSet, resolve
from movieclub.users.models import User
from movieclub.users.tests.factories import create_user

_faker = faker.Faker()


def create_review(
    *, release: Release = NotSet, user: User = NotSet, comment: str = NotSet, **kwargs
) -> Review:
    return Review.objects.create(
        release=resolve(release, create_movie),
        user=resolve(user, create_user),
        comment=resolve(comment, _faker.text(60)),
        **kwargs,
    )
