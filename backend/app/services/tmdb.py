import os

import requests
from dotenv import load_dotenv

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

NETFLIX_PROVIDER_ID = 8


def _get_genre_map() -> dict[int, str]:
    response = requests.get(
        f"{TMDB_BASE_URL}/genre/movie/list",
        params={"api_key": TMDB_API_KEY, "language": "ko-KR"},
        timeout=10,
    )
    response.raise_for_status()
    return {genre["id"]: genre["name"] for genre in response.json()["genres"]}


def _get_runtime(movie_id: int) -> int | None:
    response = requests.get(
        f"{TMDB_BASE_URL}/movie/{movie_id}",
        params={"api_key": TMDB_API_KEY, "language": "ko-KR"},
        timeout=10,
    )
    response.raise_for_status()
    return response.json().get("runtime")


def get_netflix_movies(count: int = 10) -> list[dict]:
    response = requests.get(
        f"{TMDB_BASE_URL}/discover/movie",
        params={
            "api_key": TMDB_API_KEY,
            "with_watch_providers": NETFLIX_PROVIDER_ID,
            "watch_region": "KR",
            "sort_by": "popularity.desc",
            "language": "ko-KR",
        },
        timeout=10,
    )
    response.raise_for_status()
    results = response.json().get("results", [])[:count]

    genre_map = _get_genre_map()

    contents = []
    for movie in results:
        poster_path = movie.get("poster_path")
        contents.append(
            {
                "title": movie.get("title"),
                "genre": [genre_map.get(gid, "") for gid in movie.get("genre_ids", [])],
                "runtime": _get_runtime(movie["id"]),
                "poster_url": f"{TMDB_IMAGE_BASE_URL}{poster_path}" if poster_path else None,
                "overview": movie.get("overview"),
            }
        )

    return contents
