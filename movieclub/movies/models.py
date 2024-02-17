from __future__ import annotations

from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVectorField
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django_countries.fields import CountryField

from movieclub.reviews.models import BaseReview


class Genre(models.Model):
    """A movie genre."""

    name = models.CharField(max_length=30, unique=True)
    tmdb_id = models.PositiveIntegerField(unique=True)

    def __str__(self) -> str:
        """Genre name."""
        return self.name

    def get_absolute_url(self) -> str:
        """Return genre detail URL."""
        return reverse(
            "movies:genre_detail",
            kwargs={
                "genre_id": self.pk,
                "slug": slugify(self.name),
            },
        )


class MovieQuerySet(models.QuerySet):
    """QuerySet for Movie model."""

    def search(self, search_term: str) -> MovieQuerySet:
        """Does a full text search"""
        if not search_term:
            return self.none()
        query = SearchQuery(search_term, search_type="websearch")

        return self.annotate(
            rank=SearchRank(models.F("search_vector"), query=query)
        ).filter(search_vector=query)


class Movie(models.Model):
    """Movie details."""

    title = models.CharField(max_length=120)
    original_title = models.CharField(max_length=120, blank=True)

    tagline = models.TextField(blank=True)
    overview = models.TextField(blank=True)

    tmdb_id = models.BigIntegerField(unique=True)
    imdb_id = models.CharField(max_length=12, blank=True)

    genres = models.ManyToManyField(Genre, blank=True, related_name="movies")

    homepage = models.URLField(blank=True)

    backdrop_url = models.URLField(blank=True)
    poster_url = models.URLField(blank=True)

    language = models.CharField(max_length=2, default="en")

    release_date = models.DateField(null=True, blank=True)

    runtime = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Runtime (minutes)",
    )

    search_vector = SearchVectorField(null=True, editable=False)

    countries = CountryField(multiple=True)

    objects = MovieQuerySet.as_manager()

    def __str__(self) -> str:
        """Returns title."""
        return self.title

    def get_absolute_url(self) -> str:
        """Returns detail url."""

        return reverse(
            "movies:movie_detail",
            kwargs={
                "slug": slugify(self.title),
                "movie_id": self.pk,
            },
        )


class CastMember(models.Model):
    """A cast or crew member"""

    movie = models.ForeignKey(
        Movie,
        related_name="cast_members",
        on_delete=models.CASCADE,
    )
    person = models.ForeignKey(
        "credits.Person",
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
        "credits.Person",
        related_name="movies_as_crew_member",
        on_delete=models.CASCADE,
    )
    job = models.CharField(max_length=120)

    def __str__(self) -> str:
        """Returns job."""
        return self.job


class Review(BaseReview):
    """Move review."""

    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    def get_target_id(self) -> str:
        """Return target in DOM"""
        return f"review-movie-{self.pk}"

    def get_edit_url(self) -> str:
        """URL to edit endpoint."""
        return reverse("movies:edit_review", kwargs={"review_id": self.pk})

    def get_delete_url(self) -> str:
        """URL to delete endpoint."""
        return reverse("movies:delete_review", kwargs={"review_id": self.pk})
