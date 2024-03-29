import datetime

import faker
from django.utils import timezone

from movieclub.blogathons.models import Blogathon, Entry, Proposal
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


def create_proposal(
    *,
    blogathon: Blogathon = NotSet,
    participant: User = NotSet,
    proposal: str = NotSet,
    **kwargs,
) -> Proposal:
    return Proposal.objects.create(
        blogathon=resolve(
            blogathon,
            create_blogathon,
        ),
        participant=resolve(participant, create_user),
        proposal=resolve(proposal, lambda: _faker.text(100)),
        **kwargs,
    )


def create_entry(
    *,
    blogathon: Blogathon = NotSet,
    participant: User = NotSet,
    blog_title: str = NotSet,
    blog_url: str = NotSet,
    **kwargs,
) -> Proposal:
    return Entry.objects.create(
        blogathon=resolve(
            blogathon,
            create_blogathon,
        ),
        participant=resolve(participant, create_user),
        blog_title=resolve(blog_title, lambda: _faker.text(100)),
        blog_url=resolve(blog_title, _faker.url),
        **kwargs,
    )
