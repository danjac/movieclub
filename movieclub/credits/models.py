from django.db import models
from django.utils.text import slugify


class Person(models.Model):
    """A crew or cast member."""

    class Gender(models.IntegerChoices):
        UNSPECIFIED = 0, "Unspecified"
        FEMALE = 1, "Female"
        MALE = 2, "Male"

    tmdb_id = models.BigIntegerField(unique=True)
    name = models.CharField(max_length=120)
    gender = models.PositiveSmallIntegerField(choices=Gender)
    profile_url = models.URLField(blank=True)

    def __str__(self) -> str:
        """Return person's name."""
        return self.name

    @property
    def slug(self) -> str:
        """Return name as slug"""
        return slugify(self.name)
