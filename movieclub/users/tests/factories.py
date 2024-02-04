from allauth.account.models import EmailAddress
from faker import Faker

from movieclub.tests.factories import NotSet, resolve
from movieclub.users.models import User

_faker = Faker()


def create_user(
    **kwargs,
) -> User:
    return User.objects.create_user(**_user_kwargs(**kwargs))


async def acreate_user(
    **kwargs,
) -> User:
    return await User.objects.acreate_user(**_user_kwargs(**kwargs))


def create_email_address(
    *,
    user: User = NotSet,
    email: str = NotSet,
    verified: bool = True,
    primary: bool = False,
) -> EmailAddress:
    return EmailAddress.objects.create(
        user=resolve(user, create_user),
        email=resolve(email, _faker.unique.email),
        verified=verified,
        primary=primary,
    )


def _user_kwargs(
    *,
    username: str = NotSet,
    email: str = NotSet,
    password: str = NotSet,
    **kwargs,
) -> dict:
    return dict(
        username=resolve(username, _faker.unique.user_name),
        email=resolve(email, _faker.unique.email),
        password=resolve(password, "testpass1"),
        **kwargs,
    )
