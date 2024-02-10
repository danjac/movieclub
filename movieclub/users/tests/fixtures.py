import pytest
from django.contrib.auth.models import AnonymousUser
from django.test import Client

from movieclub.users.models import User
from movieclub.users.tests.factories import create_user


@pytest.fixture()
def user() -> User:
    return create_user()


@pytest.fixture()
def user_with_keypair() -> User:
    return create_user(with_keypair=True)


@pytest.fixture()
def anonymous_user() -> AnonymousUser:
    return AnonymousUser()


@pytest.fixture()
def auth_user(client: Client, user: User) -> User:
    client.force_login(user)
    return user


@pytest.fixture()
def auth_user_with_keypair(client: Client, user_with_keypair: User) -> User:
    client.force_login(user_with_keypair)
    return user_with_keypair


@pytest.fixture()
def staff_user(client: Client) -> User:
    user = create_user(is_staff=True)
    client.force_login(user)
    return user
