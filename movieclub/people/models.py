from django.db import models


class Person(models.Model):
    """A crew or cast member."""

    class Gender(models.TextChoice):
        MALE = "male", "Male"
        FEMALE = "female", "Female"
        UNSPECIFIED = "unspecified", "Unspecified"

    tmdb_id = models.BigIntegerField(unique=True)
    name = models.CharField(max_length=30)
    gender = models.CharField(max_length=12, choices=Gender)
    profile = models.URLField(blank=True)

    def __str__(self) -> str:
        """Return person's name."""
        return self.name
