from __future__ import annotations

from django.contrib.auth.models import AbstractUser, BaseUserManager
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

    bio = models.TextField(blank=True)

    objects: models.Manager[User] = UserManager()


class Link(models.Model):
    """Link to user's webpage or social media etc."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="links")

    title = models.CharField(max_length=12)
    url = models.URLField()

    def __str__(self) -> str:
        """Return the URL"""
        return self.url
