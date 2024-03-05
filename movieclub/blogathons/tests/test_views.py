import datetime
import http

import pytest
from django.urls import reverse, reverse_lazy
from django.utils import timezone

from movieclub.blogathons.models import Blogathon, Entry, Proposal
from movieclub.blogathons.tests.factories import create_blogathon, create_proposal
from movieclub.tests.factories import create_batch


@pytest.fixture()
def auth_user_blogathon(auth_user):
    return create_blogathon(organizer=auth_user)


@pytest.fixture()
def proposal(auth_user_blogathon):
    return create_proposal(blogathon=auth_user_blogathon)


class TestBlogathonList:
    url = reverse_lazy("blogathons:blogathon_list")

    @pytest.mark.django_db()
    def test_get(self, client):
        create_batch(create_blogathon, 3)
        response = client.get(self.url)
        assert response.status_code == http.HTTPStatus.OK


class TestAddBlogathon:
    url = reverse_lazy("blogathons:add_blogathon")

    @pytest.mark.django_db()
    def test_get(self, client, auth_user):
        response = client.get(self.url)
        assert response.status_code == http.HTTPStatus.OK

    @pytest.mark.django_db()
    def test_post(self, client, auth_user):
        starts = timezone.now() + datetime.timedelta(days=7)
        ends = starts + datetime.timedelta(days=14)
        response = client.post(
            self.url,
            {
                "starts": starts.strftime("%Y-%m-%d"),
                "ends": ends.strftime("%Y-%m-%d"),
                "name": "test",
                "description": "test",
            },
        )
        assert response.url == reverse("blogathons:blogathon_list")

        blogathon = Blogathon.objects.get()
        assert blogathon.organizer == auth_user


class TestEditBlogathon:
    @pytest.fixture()
    def url(self, auth_user_blogathon):
        return reverse("blogathons:edit_blogathon", args=[auth_user_blogathon.pk])

    @pytest.mark.django_db()
    def test_get(self, client, url):
        response = client.get(url)
        assert response.status_code == http.HTTPStatus.OK

    @pytest.mark.django_db()
    def test_post(self, client, auth_user_blogathon, url):
        starts = timezone.now() + datetime.timedelta(days=7)
        ends = starts + datetime.timedelta(days=14)
        response = client.post(
            url,
            {
                "starts": starts.strftime("%Y-%m-%d"),
                "ends": ends.strftime("%Y-%m-%d"),
                "name": "test",
                "description": "test",
            },
        )

        auth_user_blogathon.refresh_from_db()

        assert response.url == auth_user_blogathon.get_absolute_url()
        assert auth_user_blogathon.name == "test"


class TestBlogathonDetail:
    @pytest.mark.django_db()
    def test_get(self, client, auth_user, public_blogathon):
        response = client.get(public_blogathon.get_absolute_url())
        assert response.status_code == http.HTTPStatus.OK

    @pytest.mark.django_db()
    def test_get_organizer(self, client, auth_user_blogathon):
        response = client.get(auth_user_blogathon.get_absolute_url())
        assert response.status_code == http.HTTPStatus.OK


class TestBlogathonProposals:
    @pytest.mark.django_db()
    def test_get(self, client, auth_user_blogathon):
        response = client.get(
            reverse("blogathons:blogathon_proposals", args=[auth_user_blogathon.pk])
        )
        assert response.status_code == http.HTTPStatus.OK


class TestSubmitProposal:
    @pytest.fixture()
    def url(self, public_blogathon):
        return reverse("blogathons:submit_proposal", args=[public_blogathon.pk])

    @pytest.mark.django_db()
    def test_get(self, client, auth_user, url):
        response = client.get(url)
        assert response.status_code == http.HTTPStatus.OK

    @pytest.mark.django_db()
    def test_get_not_allowed(self, client, auth_user, public_blogathon, url):
        create_proposal(participant=auth_user, blogathon=public_blogathon)
        response = client.get(url)
        assert response.status_code == http.HTTPStatus.FORBIDDEN

    @pytest.mark.django_db()
    def test_post(self, client, auth_user, public_blogathon, url):
        response = client.post(url, {"proposal": "test"})
        proposal = public_blogathon.proposals.get()
        assert response.url == proposal.get_absolute_url()


class TestPublishBlogathon:
    @pytest.mark.django_db()
    def test_post(self, client, auth_user_blogathon):
        response = client.post(
            reverse("blogathons:publish_blogathon", args=[auth_user_blogathon.pk])
        )
        assert response.url == auth_user_blogathon.get_absolute_url()
        auth_user_blogathon.refresh_from_db()
        assert auth_user_blogathon.published


class TestProposalDetail:
    @pytest.mark.django_db()
    def test_get_organizer(self, client, proposal):
        response = client.get(proposal.get_absolute_url())
        assert response.status_code == http.HTTPStatus.OK

    @pytest.mark.django_db()
    def test_get_participant(self, client, auth_user):
        proposal = create_proposal(participant=auth_user)
        response = client.get(proposal.get_absolute_url())
        assert response.status_code == http.HTTPStatus.OK

    @pytest.mark.django_db()
    def test_get_non_participant(self, client, auth_user):
        proposal = create_proposal()
        response = client.get(proposal.get_absolute_url())
        assert response.status_code == http.HTTPStatus.NOT_FOUND


class TestRespondToProposal:
    @pytest.fixture()
    def url(self, proposal):
        return reverse("blogathons:respond_to_proposal", args=[proposal.pk])

    @pytest.mark.django_db()
    def test_get(self, client, proposal, url):
        response = client.get(url)
        assert response.status_code == http.HTTPStatus.OK

    @pytest.mark.django_db()
    def test_post_accept(self, client, proposal):
        response = client.post(
            reverse("blogathons:respond_to_proposal", args=[proposal.pk]),
            {"response": "ok", "action": "accept"},
        )
        assert response.url == proposal.get_absolute_url()
        proposal.refresh_from_db()
        assert proposal.status_changed_at
        assert proposal.is_accepted()
        assert proposal.response == "ok"

    @pytest.mark.django_db()
    def test_post_reject(self, client, proposal):
        response = client.post(
            reverse("blogathons:respond_to_proposal", args=[proposal.pk]),
            {"response": "ok", "action": "reject"},
        )

        assert response.url == proposal.get_absolute_url()
        proposal.refresh_from_db()
        assert proposal.status_changed_at
        assert proposal.is_rejected()
        assert proposal.response == "ok"

    @pytest.mark.django_db()
    def test_post_unknown(self, client, proposal):
        response = client.post(
            reverse("blogathons:respond_to_proposal", args=[proposal.pk]),
            {"response": "ok", "action": "one"},
        )
        assert response.status_code == http.HTTPStatus.BAD_REQUEST
        proposal.refresh_from_db()
        assert proposal.is_submitted()


class TestSubmitEntry:
    @pytest.fixture()
    def proposal(self, open_blogathon, auth_user):
        return create_proposal(
            blogathon=open_blogathon,
            participant=auth_user,
            status=Proposal.Status.ACCEPTED,
        )

    @pytest.fixture()
    def url(self, open_blogathon):
        return reverse("blogathons:submit_entry", args=[open_blogathon.pk])

    @pytest.mark.django_db()
    def test_get(self, client, proposal, url):
        response = client.get(url)
        assert response.status_code == http.HTTPStatus.OK

    @pytest.mark.django_db()
    def test_get_permission_denied(self, client, auth_user, url):
        response = client.get(url)
        assert response.status_code == http.HTTPStatus.FORBIDDEN

    @pytest.mark.django_db()
    def test_post(self, client, proposal, open_blogathon, auth_user, url):
        response = client.post(
            url,
            {
                "blog_title": "test",
                "blog_url": "https://example.com",
                "blog_summary": "test",
            },
        )
        assert response.url == open_blogathon.get_absolute_url()

        entry = Entry.objects.get()
        assert entry.participant == auth_user
