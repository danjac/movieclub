import pytest

from movieclub.activitypub.models import Actor
from movieclub.activitypub.signals import populate_actor


class TestPopulateActor:
    @pytest.mark.django_db()
    def test_populate_actor(self, rf, site, site_instance, user):
        request = rf.get("/")
        request.site = site

        populate_actor(request, user)

        actor = Actor.objects.get()
        assert actor.instance == site_instance
        assert actor.handle == user.username

    @pytest.mark.django_db()
    def test_populate_actor_no_instance(self, rf, site, user):
        request = rf.get("/")
        request.site = site

        populate_actor(request, user)

        assert Actor.objects.exists() is False
