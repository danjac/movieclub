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

    country_codes = ",".join(
        [c["iso_3166_1"] for c in result.get("production_countries", [])]
    )

    movie = await Movie.objects.acreate(
        tmdb_id=tmdb_id,
        countries=country_codes,
        imdb_id=result["imdb_id"],
        title=result["title"],
        original_title=result["original_title"],
        tagline=result["tagline"],
        overview=result["overview"],
        language=result["original_language"],
        runtime=result["runtime"],
        homepage=result["homepage"] or "",
        release_date=arrow.get(result["release_date"], "YYYY-MM-DD").date()
        if result["release_date"]
        else None,
        backdrop=tmdb.get_image_url(result["backdrop_path"])
        if result["backdrop_path"]
        else "",
        poster=tmdb.get_image_url(result["poster_path"])
        if result["poster_path"]
        else "",
    )

    genre_dcts = result.get("genres", [])

    # TBD: django command to prefetch all movie genres
    await Genre.objects.abulk_create(
        [Genre(tmdb_id=genre["id"], name=genre["name"]) for genre in genre_dcts],
        ignore_conflicts=True,
    )

    # refetch genres

    genres = []

    async for genre in Genre.objects.filter(tmdb_id__in={g["id"] for g in genre_dcts}):
        genres.append(genre)

    await movie.genres.aset(genres)

    # get credits

    credits = await tmdb.get_movie_credits(client, tmdb_id)

    # extract all the people first

    persons: list[Person] = []

    cast_dct = credits.get("cast", [])
    crew_dct = credits.get("crew", [])

    persons += [_get_person_from_credit(credit) for credit in cast_dct]
    persons += [_get_person_from_credit(credit) for credit in crew_dct]

    await Person.objects.abulk_create(persons, ignore_conflicts=True)

    persons_dct: dict[int, Person] = {}

    async for person in Person.objects.filter(tmdb_id__in={p.tmdb_id for p in persons}):
        persons_dct[person.tmdb_id] = person

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

    return movie, True


def _get_person_from_credit(credit: dict) -> Person:
    return Person(
        tmdb_id=credit["id"],
        gender=credit["gender"],
        name=credit["name"],
        profile=tmdb.get_image_url(credit["profile_path"])
        if credit["profile_path"]
        else "",
    )
