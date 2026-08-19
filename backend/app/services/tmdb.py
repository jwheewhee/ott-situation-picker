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


def _discover_pages(media_type: str, count: int) -> list[dict]:
    results: list[dict] = []
    page = 1

    while len(results) < count:
        response = requests.get(
            f"{TMDB_BASE_URL}/discover/{media_type}",
            params={
                "api_key": TMDB_API_KEY,
                "with_watch_providers": NETFLIX_PROVIDER_ID,
                "watch_region": "KR",
                "sort_by": "popularity.desc",
                "vote_count.gte": 100,
                "language": "ko-KR",
                "page": page,
            },
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()

        page_results = data.get("results", [])
        if not page_results:
            break
        results.extend(page_results)

        total_pages = data.get("total_pages", page)
        if page >= total_pages:
            break
        page += 1

    return results[:count]


def _build_movie_content(movie: dict, genre_map: dict[int, str]) -> dict:
    poster_path = movie.get("poster_path")
    return {
        "title": movie.get("title"),
        "genre": [genre_map.get(gid, "") for gid in movie.get("genre_ids", [])],
        "runtime": _get_runtime(movie["id"]),
        "poster_url": f"{TMDB_IMAGE_BASE_URL}{poster_path}" if poster_path else None,
        "overview": movie.get("overview"),
        "content_type": "movie",
    }


def _build_tv_content(show: dict, genre_map: dict[int, str]) -> dict:
    poster_path = show.get("poster_path")
    return {
        "title": show.get("name"),
        "genre": [genre_map.get(gid, "") for gid in show.get("genre_ids", [])],
        "episode_run_time": _get_episode_run_time(show["id"]),
        "poster_url": f"{TMDB_IMAGE_BASE_URL}{poster_path}" if poster_path else None,
        "overview": show.get("overview"),
        "content_type": "tv",
    }


def get_netflix_movies(count: int = 50) -> list[dict]:
    results = _discover_pages("movie", count)
    genre_map = _get_movie_genre_map()
    return [_build_movie_content(movie, genre_map) for movie in results]


def get_netflix_tv(count: int = 50) -> list[dict]:
    results = _discover_pages("tv", count)
    genre_map = _get_tv_genre_map()
    return [_build_tv_content(show, genre_map) for show in results]


def _search_movie(query: str) -> dict | None:
    response = requests.get(
        f"{TMDB_BASE_URL}/search/movie",
        params={"api_key": TMDB_API_KEY, "query": query, "language": "ko-KR"},
        timeout=10,
    )
    response.raise_for_status()
    results = response.json().get("results", [])
    return results[0] if results else None


def _search_tv(query: str) -> dict | None:
    response = requests.get(
        f"{TMDB_BASE_URL}/search/tv",
        params={"api_key": TMDB_API_KEY, "query": query, "language": "ko-KR"},
        timeout=10,
    )
    response.raise_for_status()
    results = response.json().get("results", [])
    return results[0] if results else None


def get_metadata_for_titles(titles: list[dict]) -> list[dict]:
    """Look up TMDB metadata for entries like those from
    netflix_top10.get_netflix_top10_titles() - each a dict with at least
    "title" and "content_type" ("movie" or "tv"). Titles with no TMDB match
    are skipped.
    """
    movie_genre_map = _get_movie_genre_map()
    tv_genre_map = _get_tv_genre_map()

    contents = []
    for item in titles:
        query = item.get("title")
        content_type = item.get("content_type")
        if not query or content_type not in ("movie", "tv"):
            continue

        if content_type == "movie":
            match = _search_movie(query)
            if match is None:
                continue
            contents.append(_build_movie_content(match, movie_genre_map))
        else:
            match = _search_tv(query)
            if match is None:
                continue
            contents.append(_build_tv_content(match, tv_genre_map))

    return contents
