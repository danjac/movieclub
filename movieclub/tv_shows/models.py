from django.contrib.postgres.search import SearchVectorField
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django_countries.fields import CountryField

from movieclub.credits.models import BaseCastMember, BaseCrewMember
from movieclub.reviews.models import BaseReview


class Genre(models.Model):
    """A TV show genre."""

    name = models.CharField(max_length=30, unique=True)
    tmdb_id = models.PositiveIntegerField(unique=True)

    def __str__(self) -> str:
        """Genre name."""
        return self.name

    def get_absolute_url(self) -> str:
        """Return genre detail URL."""
        return reverse(
            "tv_shows:genre_detail",
            kwargs={
                "genre_id": self.pk,
                "slug": slugify(self.name),
            },
        )


class TVShow(models.Model):
    """TV show model."""

    title = models.CharField(max_length=120)

    tagline = models.TextField(blank=True)
    overview = models.TextField(blank=True)

    tmdb_id = models.BigIntegerField(unique=True)

    genres = models.ManyToManyField(Genre, blank=True, related_name="movies")

    homepage = models.URLField(blank=True)

    backdrop_url = models.URLField(blank=True)
    poster_url = models.URLField(blank=True)

    release_date = models.DateField(null=True, blank=True)

    search_vector = SearchVectorField(null=True, editable=False)

    countries = CountryField(multiple=True)

    def __str__(self) -> str:
        """Returns title."""
        return self.title

    def get_absolute_url(self) -> str:
        """Returns detail url."""

        return reverse(
            "tv_shows:tv_show_detail",
            kwargs={
                "slug": slugify(self.title),
                "movie_id": self.pk,
            },
        )


class CastMember(BaseCastMember):
    """A cast or crew member"""

    tv_show = models.ForeignKey(
        TVShow,
        related_name="cast_members",
        on_delete=models.CASCADE,
    )


class CrewMember(BaseCrewMember):
    """A cast or crew member"""

    tv_show = models.ForeignKey(
        TVShow,
        related_name="crew_members",
        on_delete=models.CASCADE,
    )


class Review(BaseReview):
    """TV show review."""

    tv_show = models.ForeignKey(
        TVShow,
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    def get_target_id(self) -> str:
        """Return target in DOM"""
        return f"review-tv-shows-{self.pk}"

    def get_edit_url(self) -> str:
        """URL to edit endpoint."""
        return reverse("tv_shows:edit_review", kwargs={"review_id": self.pk})

    def get_delete_url(self) -> str:
        """URL to delete endpoint."""
        return reverse("tv_shows:delete_review", kwargs={"review_id": self.pk})
