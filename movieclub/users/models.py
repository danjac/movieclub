from __future__ import annotations

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

from movieclub.activitypub.signature import create_key_pair


class UserManager(BaseUserManager):
    """Custom Manager for User model."""

    def create_user(self, *args, **kwargs) -> User:
        """Create new user."""
        user = self._make_user(*args, **kwargs)
        user.save(using=self._db)

        return user

    async def acreate_user(self, *args, **kwargs) -> User:
        """Create new user."""
        user = self._make_user(*args, **kwargs)
        await user.asave(using=self._db)

        return user

    def _make_user(
        self,
        username: str,
        email: str,
        password: str | None = None,
        **kwargs,
    ) -> User:
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            **kwargs,
        )
        user.set_password(password)
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

    def save(self, **kwargs) -> None:
        """Overrides save() method of user to auto-generate keypair."""
        if not self.private_key or not self.public_key:
            self.private_key, self.public_key = create_key_pair()
        super().save(**kwargs)
