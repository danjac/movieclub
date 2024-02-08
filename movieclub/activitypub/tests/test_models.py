import pytest

from movieclub.activitypub.models import Actor, Instance
from movieclub.activitypub.tests.factories import create_actor, create_instance


class TestInstance:
    @pytest.mark.django_db()
    def test_str(self):
        instance = Instance(domain="example.com")
        assert str(instance) == "example.com"


class TestActor:
    @pytest.mark.django_db()
    def test_local_if_remote(self, remote_actor):
        assert Actor.objects.local().exists() is False

    @pytest.mark.django_db()
    def test_local_if_local(self, actor):
        assert Actor.objects.local().exists() is True

    @pytest.mark.django_db()
    def test_get_for_resource(self, actor):
        assert Actor.objects.get_for_resource(actor.get_resource()) == actor

    @pytest.mark.django_db()
    def test_get_for_resource_acct_prefix(self, actor):
        assert Actor.objects.get_for_resource(f"acct:{actor.get_resource()}") == actor

    @pytest.mark.django_db()
    def test_get_for_invalid_resource(self, actor):
        with pytest.raises(Actor.DoesNotExist):
            assert Actor.objects.get_for_resource("tester")

    @pytest.mark.django_db()
    def test_get_for_resource_not_found(self, actor):
        with pytest.raises(Actor.DoesNotExist):
            Actor.objects.get_for_resource("tester@example.com")

    def test_str(self):
        actor = Actor(handle="tester")
        assert str(actor) == "tester"

    @pytest.mark.django_db()
    def test_get_resource(self):
        actor = create_actor(
            instance=create_instance(domain="example.com"),
            handle="tester",
        )
        assert actor.get_resource() == "tester@example.com"
