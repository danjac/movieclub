from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.auth.models import AbstractUser, BaseUserManager

if TYPE_CHECKING:  # pragma: no cover
    from django.db import models


class UserManager(BaseUserManager):
    """Custom Manager for User model."""

    def create_user(
        self,
        *,
        username: str,
        email: str,
        password: str | None = None,
        **kwargs,
    ) -> User:
        """Create new user."""
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            **kwargs,
        )

        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self, *args, **kwargs) -> User:
        """Create new superuser."""
        return self.create_user(
            *args,
            is_staff=True,
            is_superuser=True,
            **kwargs,
        )


class User(AbstractUser):
    """Custom User model."""

    objects: models.Manager[User] = UserManager()
