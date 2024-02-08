import pytest

from movieclub.activitypub.tests.factories import create_actor, create_instance


@pytest.fixture()
def site_instance(site):
    return create_instance(domain=site.domain, local=True)


@pytest.fixture()
def instance(site):
    return create_instance()


@pytest.fixture()
def actor():
    return create_actor()


@pytest.fixture()
def remote_actor():
    return create_actor(instance=create_instance(local=False))
