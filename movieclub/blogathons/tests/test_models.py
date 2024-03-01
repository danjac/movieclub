import datetime

import pytest
from django.utils import timezone

from movieclub.blogathons.models import Blogathon, Proposal
from movieclub.blogathons.tests.factories import (
    create_blogathon,
    create_entry,
    create_proposal,
)


class TestBlogathon:
    @pytest.mark.django_db()
    def test_for_organizer(self, blogathon):
        assert Blogathon.objects.for_organizer(blogathon.organizer).exists()

    @pytest.mark.django_db()
    def test_for_organizer_other_user(self, blogathon, user):
        assert not Blogathon.objects.for_organizer(user).exists()

    @pytest.mark.django_db()
    def test_for_organizer_anonymous_user(self, blogathon, anonymous_user):
        assert not Blogathon.objects.for_organizer(anonymous_user).exists()

    @pytest.mark.django_db()
    def test_draft_available_for_user(self, blogathon):
        assert Blogathon.objects.available(blogathon.organizer).exists()

    @pytest.mark.django_db()
    def test_draft_available_for_other_user(self, blogathon, user):
        assert not Blogathon.objects.available(user).exists()

    @pytest.mark.django_db()
    def test_published_available_for_user(self, public_blogathon):
        assert Blogathon.objects.available(public_blogathon.organizer).exists()

    @pytest.mark.django_db()
    def test_published_available_for_other_user(self, public_blogathon, user):
        assert Blogathon.objects.available(user).exists()

    @pytest.mark.django_db()
    def test_published_available_for_anonymous_user(
        self, public_blogathon, anonymous_user
    ):
        assert Blogathon.objects.available(anonymous_user).exists()

    @pytest.mark.django_db()
    def test_can_submit_entry_too_early(self, public_blogathon, user):
        create_proposal(
            participant=user,
            blogathon=public_blogathon,
            status=Proposal.Status.ACCEPTED,
        )
        assert not public_blogathon.can_submit_entry(user)

    @pytest.mark.django_db()
    def test_can_submit_entry_too_late(self, user):
        now = timezone.now()
        blogathon = create_blogathon(
            published=now,
            starts=now.date() - datetime.timedelta(days=14),
            ends=now.date() - datetime.timedelta(days=1),
        )
        create_proposal(
            participant=user,
            blogathon=blogathon,
            status=Proposal.Status.ACCEPTED,
        )
        assert not blogathon.can_submit_entry(user)

    @pytest.mark.django_db()
    def test_can_submit_entry_ok(self, open_blogathon, user, accepted_proposal):
        assert open_blogathon.can_submit_entry(user)

    @pytest.mark.django_db()
    def test_can_submit_entry_is_organizer(self, open_blogathon):
        assert open_blogathon.can_submit_entry(open_blogathon.organizer)

    @pytest.mark.django_db()
    def test_can_submit_entry_already_submitted(
        self, open_blogathon, user, accepted_proposal
    ):
        create_entry(blogathon=open_blogathon, participant=user)
        assert not open_blogathon.can_submit_entry(user)

    @pytest.mark.django_db()
    def test_can_submit_proposal_ok(self, public_blogathon, user):
        assert public_blogathon.can_submit_proposal(user)

    @pytest.mark.django_db()
    def test_can_submit_proposal_already_submitted(self, public_blogathon, user):
        create_proposal(participant=user, blogathon=public_blogathon)
        assert not public_blogathon.can_submit_proposal(user)

    @pytest.mark.django_db()
    def test_can_submit_proposal_user_is_organizer(self, public_blogathon):
        assert not public_blogathon.can_submit_proposal(public_blogathon.organizer)

    @pytest.mark.django_db()
    def test_can_submit_proposal_has_ended(self, user):
        now = timezone.now()
        blogathon = create_blogathon(
            ends=(now - datetime.timedelta(days=7)).date(), published=now
        )
        assert not blogathon.can_submit_proposal(user)

    @pytest.mark.django_db()
    def test_can_submit_proposal_user_not_published(self, blogathon, user):
        assert not blogathon.can_submit_proposal(user)
