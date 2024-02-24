import datetime

import pytest
from django.utils import timezone

from movieclub.blogathons.tests.factories import create_blogathon


@pytest.fixture()
def blogathon():
    return create_blogathon()


@pytest.fixture()
def public_blogathon():
    return create_blogathon(published=timezone.now())


class TestBlogathon:
    @pytest.mark.django_db()
    def test_can_submit_proposal_ok(self, public_blogathon, user):
        assert public_blogathon.can_submit_proposal(user)

    @pytest.mark.django_db()
    def test_can_submit_proposal_user_is_organizer(self, public_blogathon):
        assert not public_blogathon.can_submit_proposal(public_blogathon.organizer)

    @pytest.mark.django_db()
    def test_can_submit_proposal_has_started(self, user):
        blogathon = create_blogathon(starts=timezone.now() - datetime.timedelta(days=7))
        assert not blogathon.can_submit_proposal(user)

    @pytest.mark.django_db()
    def test_can_submit_proposal_user_not_published(self, blogathon, user):
        assert not blogathon.can_submit_proposal(user)
