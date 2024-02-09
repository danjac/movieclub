import pytest

from movieclub.activitypub.models import Actor, Instance
from movieclub.activitypub.tests.factories import create_actor, create_instance


class TestInstance:
    @pytest.mark.django_db()
    def test_str(self):
        instance = Instance(domain="example.com")
        assert str(instance) == "example.com"


class TestActor:
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
