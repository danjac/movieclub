import json
import pathlib

MOCKS_DIR = pathlib.Path(__file__).parent / "json"


def movie_json() -> dict:
    return json.load((MOCKS_DIR / "movie.json").open("r"))


def credits_json() -> dict:
    return json.load((MOCKS_DIR / "credits.json").open("r"))


def search_results_json() -> dict:
    return json.load((MOCKS_DIR / "search_results.json").open("r"))
