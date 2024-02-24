import datetime

import faker
from django.utils import timezone

from movieclub.blogathons.models import Blogathon
from movieclub.tests.factories import NotSet, resolve
from movieclub.users.models import User
from movieclub.users.tests.factories import create_user

_faker = faker.Faker()


def create_blogathon(
    *,
    name: str = NotSet,
    organizer: User = NotSet,
    starts: datetime.date = NotSet,
    ends: datetime.date = NotSet,
    **kwargs,
) -> Blogathon:
    now = timezone.now().date()
    return Blogathon.objects.create(
        name=resolve(name, lambda: _faker.text(60)),
        organizer=resolve(organizer, create_user),
        starts=resolve(starts, lambda: now + datetime.timedelta(days=7)),
        ends=resolve(ends, lambda: now + datetime.timedelta(days=21)),
        **kwargs,
    )
