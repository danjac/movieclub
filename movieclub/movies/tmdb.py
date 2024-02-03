import arrow
import httpx

from movieclub import tmdb
from movieclub.movies.models import CastMember, CrewMember, Genre, Movie
from movieclub.people.models import Person


async def get_or_create_movie(
    client: httpx.AsyncClient, tmdb_id: int
) -> tuple[Movie, bool]:
    """Fetches movie from TmDB if it does not already exist.
    Also fetches details on cast and crew members.

    Returns tuple (movie, created).
    """

    movie = await Movie.objects.filter(tmdb_id=tmdb_id).afirst()

    if movie is not None:
        return movie, False

    result = await tmdb.get_movie(client, tmdb_id)

    movie = await _create_movie(tmdb_id, result)

    await _add_genres(client, movie, result)
    await _add_credits(client, movie)

    return movie, True


async def _create_movie(tmdb_id: int, tmdb_result: dict) -> Movie:
    return await Movie.objects.acreate(
        tmdb_id=tmdb_id,
        imdb_id=tmdb_result["imdb_id"],
        title=tmdb_result["title"],
        original_title=tmdb_result["original_title"],
        tagline=tmdb_result["tagline"],
        overview=tmdb_result["overview"],
        language=tmdb_result["original_language"],
        runtime=tmdb_result["runtime"],
        homepage=tmdb_result["homepage"] or "",
        release_date=arrow.get(tmdb_result["release_date"], "YYYY-MM-DD").date()
        if tmdb_result["release_date"]
        else None,
        backdrop=tmdb.get_image_url(tmdb_result["backdrop_path"])
        if tmdb_result["backdrop_path"]
        else "",
        poster=tmdb.get_image_url(tmdb_result["poster_path"])
        if tmdb_result["poster_path"]
        else "",
        countries=",".join(
            [c["iso_3166_1"] for c in tmdb_result.get("production_countries", [])]
        ),
    )


async def _add_genres(
    client: httpx.AsyncClient, movie: Movie, tmdb_result: dict
) -> None:
    genre_dcts = tmdb_result.get("genres", [])

    # TBD: django command to prefetch all movie genres
    await Genre.objects.abulk_create(
        [
            Genre(
                tmdb_id=genre["id"],
                name=genre["name"],
            )
            for genre in genre_dcts
        ],
        ignore_conflicts=True,
    )

    # refetch genres

    genres = []

    async for genre in Genre.objects.filter(tmdb_id__in={g["id"] for g in genre_dcts}):
        genres.append(genre)

    await movie.genres.aset(genres)


async def _add_credits(client: httpx.AsyncClient, movie: Movie) -> None:
    credits = await tmdb.get_movie_credits(client, movie.tmdb_id)

    cast_dct = credits.get("cast", [])
    crew_dct = credits.get("crew", [])

    persons: list[Person] = []

    persons += [_get_person_from_credit(credit) for credit in cast_dct]
    persons += [_get_person_from_credit(credit) for credit in crew_dct]

    await Person.objects.abulk_create(persons, ignore_conflicts=True)

    persons_dct: dict[int, Person] = {
        person.tmdb_id: person
        async for person in Person.objects.filter(
            tmdb_id__in={p.tmdb_id for p in persons}
        )
    }

    cast_members = [
        CastMember(
            person=persons_dct[credit["id"]],
            movie=movie,
            order=credit["order"],
            character=credit["character"],
        )
        for credit in cast_dct
    ]

    await CastMember.objects.abulk_create(cast_members, ignore_conflicts=True)

    crew_members = [
        CrewMember(
            person=persons_dct[credit["id"]],
            movie=movie,
            job=credit["job"],
        )
        for credit in crew_dct
    ]

    await CrewMember.objects.abulk_create(crew_members, ignore_conflicts=True)


def _get_person_from_credit(credit: dict) -> Person:
    return Person(
        tmdb_id=credit["id"],
        gender=credit["gender"],
        name=credit["name"],
        profile=tmdb.get_image_url(credit["profile_path"])
        if credit["profile_path"]
        else "",
    )
