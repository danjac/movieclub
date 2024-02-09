import pytest

from movieclub.activitypub.tests.factories import create_actor, create_instance


@pytest.fixture()
def instance():
    return create_instance()


@pytest.fixture()
def actor(instance):
    return create_actor(instance=instance)
