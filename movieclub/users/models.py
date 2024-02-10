from __future__ import annotations

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

from movieclub.activitypub.signature import create_key_pair


class UserManager(BaseUserManager):
    """Custom Manager for User model."""

    def create_user(
        self,
        *,
        username: str,
        email: str,
        password: str | None = None,
        with_keypair: bool = True,
        **kwargs,
    ) -> User:
        """Create new user."""
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            **kwargs,
        )

        user.set_password(password)

        if with_keypair:
            user.private_key, user.public_key = create_key_pair()

        user.save(using=self._db)

        return user

    def create_superuser(self, *args, **kwargs) -> User:
        """Create new superuser."""
        return self.create_user(
            *args,
            **kwargs,
            is_staff=True,
            is_superuser=True,
        )


class User(AbstractUser):
    """Custom User model."""

    objects: models.Manager[User] = UserManager()

    # ActivityPub keys
    private_key = models.TextField(blank=True)
    public_key = models.TextField(blank=True)
