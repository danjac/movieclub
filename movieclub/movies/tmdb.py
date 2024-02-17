import attrs
import httpx

from movieclub import tmdb
from movieclub.credits.models import Person
from movieclub.movies.models import CastMember, CrewMember, Genre, Movie


def populate_movie(client: httpx.Client, tmdb_id: int) -> Movie:
    """Generate movie from Tmdb."""
    details = tmdb.get_movie_detail(client, tmdb_id)

    fields = attrs.fields(tmdb.MovieDetail)

    movie = Movie.objects.create(
        tmdb_id=tmdb_id,
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

    movie.genres.set(Genre.objects.filter(tmdb_id__in=[g.id for g in details.genres]))

    cast_member_fields = attrs.fields(tmdb.CastMember)

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
        for member in details.cast_members
    ]

    crew_member_fields = attrs.fields(tmdb.CrewMember)

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
        for member in details.crew_members
    ]

    person_ids = [p.tmdb_id for p in persons]

    Person.objects.bulk_create(persons, ignore_conflicts=True)

    persons_dict = {p.tmdb_id: p for p in Person.objects.filter(tmdb_id__in=person_ids)}

    CastMember.objects.bulk_create(
        [
            CastMember(
                movie=movie,
                person=persons_dict[member.id],
                order=member.order,
                character=member.character,
            )
            for member in details.cast_members
        ]
    )

    CrewMember.objects.bulk_create(
        [
            CrewMember(
                movie=movie,
                person=persons_dict[member.id],
                job=member.job,
            )
            for member in details.crew_members
        ]
    )

    return movie
