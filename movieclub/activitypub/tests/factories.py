from faker import Faker

from movieclub.activitypub.models import Actor, Instance
from movieclub.tests.factories import NotSet, resolve

_faker = Faker()


def create_instance(*, domain: str = NotSet, **kwargs) -> Instance:
    return Instance.objects.create(
        domain=resolve(domain, _faker.unique.domain_name),
        **kwargs,
    )


def create_actor(
    *, instance: Instance = NotSet, handle: str = NotSet, **kwargs
) -> Actor:
    return Actor.objects.create(
        instance=resolve(instance, create_instance),
        handle=resolve(handle, _faker.unique.user_name),
        **kwargs,
    )
