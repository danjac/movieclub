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
    *,
    instance: Instance = NotSet,
    handle: str = NotSet,
    profile_url: str = NotSet,
    inbox_url: str = NotSet,
    outbox_url: str = NotSet,
    **kwargs,
) -> Actor:
    instance = resolve(instance, create_instance)
    handle = resolve(handle, _faker.unique.user_name)

    return Actor.objects.create(
        instance=instance,
        handle=handle,
        profile_url=resolve(
            profile_url, lambda: f"https://{instance.domain}/profile/{handle}"
        ),
        inbox_url=resolve(
            profile_url, lambda: f"https://{instance.domain}/inbox/{handle}"
        ),
        outbox_url=resolve(
            profile_url, lambda: f"https://{instance.domain}/outbox/{handle}"
        ),
        **kwargs,
    )
