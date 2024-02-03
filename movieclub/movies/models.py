from __future__ import annotations

from django.db import models
from django_countries.fields import CountryField


class Genre(models.Model):
    """A movie genre."""

    name = models.CharField(max_length=30, unique=True)
    tmdb_id = models.PositiveIntegerField(unique=True)

    def __str__(self) -> str:
        """Genre name."""
        return self.name


class Movie(models.Model):
    """Movie details."""

    title = models.CharField(max_length=120)
    original_title = models.CharField(max_length=120, blank=True)

    tagline = models.TextField(blank=True)
    overview = models.TextField(blank=True)

    tmdb_id = models.BigIntegerField(unique=True)
    imdb_id = models.CharField(max_length=12, blank=True)

    genres = models.ManyToManyField(Genre, blank=True)

    homepage = models.URLField(blank=True)

    backdrop = models.URLField(blank=True)
    poster = models.URLField(blank=True)

    language = models.CharField(max_length=2, default="en")

    release_date = models.DateField(null=True, blank=True)

    runtime = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Runtime (minutes)",
    )

    countries = CountryField(multiple=True)

    def __str__(self) -> str:
        """Returns title."""
        return self.title


class CastMember(models.Model):
    """A cast or crew member"""

    movie = models.ForeignKey(
        Movie,
        related_name="cast_members",
        on_delete=models.CASCADE,
    )
    person = models.ForeignKey(
        "people.Person",
        related_name="movies_as_cast_member",
        on_delete=models.CASCADE,
    )
    character = models.CharField(max_length=120)
    order = models.PositiveSmallIntegerField(null=True, blank=True)

    def __str__(self) -> str:
        """Returns character name."""
        return self.character


class CrewMember(models.Model):
    """A cast or crew member"""

    movie = models.ForeignKey(
        Movie,
        related_name="crew_members",
        on_delete=models.CASCADE,
    )
    person = models.ForeignKey(
        "people.Person",
        related_name="movies_as_crew_member",
        on_delete=models.CASCADE,
    )
    job = models.CharField(max_length=120)

    def __str__(self) -> str:
        """Returns job."""
        return self.job
