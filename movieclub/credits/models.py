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


class BaseCastMember(models.Model):
    """A cast member base class."""

    person = models.ForeignKey(
        "credits.Person",
        on_delete=models.CASCADE,
        related_name="+",
    )
    character = models.CharField(max_length=120)
    order = models.PositiveSmallIntegerField(null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        """Returns character name."""
        return self.character


class BaseCrewMember(models.Model):
    """A cast or crew member"""

    person = models.ForeignKey(
        "credits.Person",
        on_delete=models.CASCADE,
        related_name="+",
    )
    job = models.CharField(max_length=120)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        """Returns job."""
        return self.job
