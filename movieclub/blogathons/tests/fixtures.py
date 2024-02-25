import datetime

import pytest
from django.utils import timezone

from movieclub.blogathons.models import Proposal
from movieclub.blogathons.tests.factories import (
    create_blogathon,
    create_proposal,
)


@pytest.fixture()
def blogathon():
    return create_blogathon()


@pytest.fixture()
def public_blogathon():
    return create_blogathon(published=timezone.now())


@pytest.fixture()
def open_blogathon():
    return create_blogathon(
        published=timezone.now(),
        starts=timezone.now().date() - datetime.timedelta(days=7),
    )


@pytest.fixture()
def accepted_proposal(open_blogathon, user):
    return create_proposal(
        participant=user,
        blogathon=open_blogathon,
        status=Proposal.Status.ACCEPTED,
    )
