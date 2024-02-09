import pytest

from movieclub.activitypub.models import Actor
from movieclub.activitypub.tests.factories import create_actor, create_instance


@pytest.fixture()
def instance(site):
    return create_instance(domain=site.domain)


@pytest.fixture()
def remote_instance(site):
    return create_instance()


@pytest.fixture()
def actor(instance):
    return create_actor(instance=instance)


@pytest.fixture()
def auth_user_actor(auth_user, instance):
    return Actor.objects.create_for_user(auth_user, instance)


@pytest.fixture()
def remote_actor(remote_instance):
    return create_actor(instance=remote_instance)
