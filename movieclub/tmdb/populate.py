import attrs
import httpx

from movieclub.credits.models import CastMember, CrewMember, Person
from movieclub.releases.models import Genre, Release
from movieclub.tmdb import api, models


def populate_movie(client: httpx.Client, tmdb_id: int) -> Release:
    """Generate movie from Tmdb."""
    details = api.get_movie_detail(client, tmdb_id)
    fields = attrs.fields(models.MovieDetail)

    movie = Release.objects.create(
        tmdb_id=tmdb_id,
        category=Release.Category.MOVIE,
        countries=",".join([c.iso_3166_1 for c in details.production_countries]),
        backdrop_url=details.backdrop_path,
        poster_url=details.poster_path,
        language=details.original_language,
        **attrs.asdict(
            details,
            filter=attrs.filters.exclude(
                fields.backdrop_path,
                fields.cast_members,
                fields.crew_members,
                fields.genres,
                fields.original_language,
                fields.poster_path,
                fields.production_countries,
                fields.id,
            ),
        ),
    )

    _populate_genres(movie, details.genres)
    _populate_credits(movie, details.cast_members, details.crew_members)

    return movie


def populate_tv_show(client: httpx.Client, tmdb_id: int) -> Release:
    """Populate TV show."""

    details = api.get_tv_show_detail(client, tmdb_id)
    fields = attrs.fields(models.TVShowDetail)

    tv_show = Release.objects.create(
        tmdb_id=tmdb_id,
        category=Release.Category.TV_SHOW,
        title=details.name,
        release_date=details.first_air_date,
        countries=",".join(details.origin_country),
        backdrop_url=details.backdrop_path,
        poster_url=details.poster_path,
        num_episodes=details.number_of_episodes,
        num_seasons=details.number_of_seasons,
        **attrs.asdict(
            details,
            filter=attrs.filters.exclude(
                fields.backdrop_path,
                fields.cast_members,
                fields.crew_members,
                fields.genres,
                fields.poster_path,
                fields.name,
                fields.first_air_date,
                fields.last_air_date,
                fields.origin_country,
                fields.number_of_episodes,
                fields.number_of_seasons,
                fields.id,
            ),
        ),
    )

    _populate_genres(tv_show, details.genres)
    _populate_credits(tv_show, details.cast_members, details.crew_members)

    return tv_show


def _populate_genres(release: Release, genres: list[models.Genre]) -> None:
    release.genres.set(Genre.objects.filter(tmdb_id__in=[g.id for g in genres]))


def _populate_credits(
    release: Release,
    cast_members: list[models.CastMember],
    crew_members: list[models.CrewMember],
):
    cast_member_fields = attrs.fields(models.CastMember)

    persons = [
        Person(
            tmdb_id=member.id,
            profile_url=member.profile_path,
            **attrs.asdict(
                member,
                filter=attrs.filters.exclude(
                    cast_member_fields.order,
                    cast_member_fields.character,
                    cast_member_fields.profile_path,
                    cast_member_fields.id,
                ),
            ),
        )
        for member in cast_members
    ]

    crew_member_fields = attrs.fields(models.CrewMember)

    persons += [
        Person(
            tmdb_id=member.id,
            profile_url=member.profile_path,
            **attrs.asdict(
                member,
                filter=attrs.filters.exclude(
                    crew_member_fields.job,
                    crew_member_fields.profile_path,
                    crew_member_fields.id,
                ),
            ),
        )
        for member in crew_members
    ]

    person_ids = [p.tmdb_id for p in persons]

    Person.objects.bulk_create(persons, ignore_conflicts=True)

    persons_dict = {p.tmdb_id: p for p in Person.objects.filter(tmdb_id__in=person_ids)}

    CastMember.objects.bulk_create(
        [
            CastMember(
                release=release,
                person=persons_dict[member.id],
                order=member.order,
                character=member.character,
            )
            for member in cast_members
        ]
    )

    CrewMember.objects.bulk_create(
        [
            CrewMember(
                release=release,
                person=persons_dict[member.id],
                job=member.job,
            )
            for member in crew_members
        ]
    )
