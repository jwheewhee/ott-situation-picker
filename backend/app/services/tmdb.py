import os

import requests
from dotenv import load_dotenv

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

NETFLIX_PROVIDER_ID = 8


def _get_movie_genre_map() -> dict[int, str]:
    response = requests.get(
        f"{TMDB_BASE_URL}/genre/movie/list",
        params={"api_key": TMDB_API_KEY, "language": "ko-KR"},
        timeout=10,
    )
    response.raise_for_status()
    return {genre["id"]: genre["name"] for genre in response.json()["genres"]}


def _get_tv_genre_map() -> dict[int, str]:
    response = requests.get(
        f"{TMDB_BASE_URL}/genre/tv/list",
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


def _get_episode_run_time(tv_id: int) -> int | None:
    response = requests.get(
        f"{TMDB_BASE_URL}/tv/{tv_id}",
        params={"api_key": TMDB_API_KEY, "language": "ko-KR"},
        timeout=10,
    )
    response.raise_for_status()
    data = response.json()

    run_times = data.get("episode_run_time") or []
    if run_times:
        return run_times[0]

    # TMDB no longer populates episode_run_time for most shows; fall back to
    # the runtime of the most recently aired episode.
    last_episode = data.get("last_episode_to_air") or {}
    return last_episode.get("runtime")


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

    genre_map = _get_movie_genre_map()

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
                "content_type": "movie",
            }
        )

    return contents


def get_netflix_tv(count: int = 10) -> list[dict]:
    response = requests.get(
        f"{TMDB_BASE_URL}/discover/tv",
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

    genre_map = _get_tv_genre_map()

    contents = []
    for show in results:
        poster_path = show.get("poster_path")
        contents.append(
            {
                "title": show.get("name"),
                "genre": [genre_map.get(gid, "") for gid in show.get("genre_ids", [])],
                "episode_run_time": _get_episode_run_time(show["id"]),
                "poster_url": f"{TMDB_IMAGE_BASE_URL}{poster_path}" if poster_path else None,
                "overview": show.get("overview"),
                "content_type": "tv",
            }
        )

    return contents
