from __future__ import annotations

from typing import ClassVar

from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVectorField
from django.db import models
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.text import slugify
from django_countries.fields import CountryField


class Genre(models.Model):
    """A movie or TV show genre."""

    name = models.CharField(max_length=30, unique=True)
    tmdb_id = models.PositiveIntegerField(unique=True)

    def __str__(self) -> str:
        """Genre name."""
        return self.name

    def get_absolute_url(self) -> str:
        """Return genre detail URL."""
        return reverse(
            "movies:genre_detail",
            kwargs={"genre_id": self.pk, "slug": self.slug},
        )

    @cached_property
    def slug(self) -> str:
        """Returns slugified name."""

        return slugify(self.name)


class ReleaseQuerySet(models.QuerySet):
    """QuerySet for Movie model."""

    def movies(self) -> ReleaseQuerySet:
        """Returns movies only"""
        return self.filter(category=self.model.Category.MOVIE)

    def tv_shows(self) -> ReleaseQuerySet:
        """Returns tv shows only"""
        return self.filter(category=self.model.Category.TV_SHOW)

    def search(self, search_term: str) -> ReleaseQuerySet:
        """Does a full text search"""
        if not search_term:
            return self.none()
        query = SearchQuery(search_term, search_type="websearch")

        return self.annotate(
            rank=SearchRank(models.F("search_vector"), query=query)
        ).filter(search_vector=query)


class Release(models.Model):
    """Movie or TV show details."""

    class Category(models.TextChoices):
        MOVIE = "movie", "Movie"
        TV_SHOW = "tv_show", "TV Show"

    category = models.CharField(max_length=12, choices=Category.choices)

    title = models.CharField(max_length=120)
    original_title = models.CharField(max_length=120, blank=True)

    tagline = models.TextField(blank=True)
    overview = models.TextField(blank=True)

    # should be unique together with release type
    tmdb_id = models.BigIntegerField()
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

    # for TV shows
    num_seasons = models.PositiveIntegerField(default=0)
    num_episodes = models.PositiveIntegerField(default=0)

    countries = CountryField(multiple=True)

    objects = ReleaseQuerySet.as_manager()

    class Meta:
        constraints: ClassVar = [
            models.UniqueConstraint(
                fields=["category", "tmdb_id"],
                name="%(app_label)s_%(class)s_unique_tmdb_id_category",
            )
        ]

    def __str__(self) -> str:
        """Returns title."""
        return self.title

    def get_absolute_url(self) -> str:
        """Absolute url to movie or TV show detail."""

        url_name = (
            "releases:tv_show_detail"
            if self.category == self.Category.TV_SHOW
            else "releases:movie_detail"
        )

        return reverse(url_name, kwargs={"release_id": self.pk, "slug": self.slug})

    @cached_property
    def slug(self) -> str:
        """Return slug of title."""
        return slugify(self.title)
