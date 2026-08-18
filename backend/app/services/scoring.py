import math

_BASE_SCORE = 50

_LIGHT_KEYWORD_TRIGGERS = ["가벼운", "가볍", "코미디", "웃김", "웃음", "유쾌", "코믹", "개그"]
_CALM_KEYWORD_TRIGGERS = ["몰입", "잔잔함", "잔잔", "힐링", "치유", "감동"]

_ACTIVE_GENRES = {"액션", "모험", "스포츠", "음악"}
_LOW_DIALOGUE_GENRES = {"애니메이션", "다큐멘터리"}
_INTENSE_GENRES = {"스릴러", "공포"}

_SHORT_RUNTIME_PERCENTILE = 0.4


def _clamp(score: float) -> int:
    return int(max(0, min(100, round(score))))


def _keywords_match(keywords: list[str], triggers: list[str]) -> bool:
    return any(trigger in keyword or keyword in trigger for keyword in keywords for trigger in triggers)


def _effective_runtime(movie: dict) -> int | None:
    runtime = movie.get("runtime")
    if runtime is not None:
        return runtime
    return movie.get("episode_run_time")


def _short_runtime_threshold(all_movies: list[dict]) -> float | None:
    runtimes = sorted(r for r in (_effective_runtime(m) for m in all_movies) if r is not None)
    if not runtimes:
        return None

    index = max(0, math.ceil(_SHORT_RUNTIME_PERCENTILE * len(runtimes)) - 1)
    return runtimes[index]


def _score_mealtime(effective_runtime: int | None, threshold: float | None, keywords: list[str]) -> int:
    score = _BASE_SCORE

    if effective_runtime is not None and threshold is not None and effective_runtime <= threshold:
        score += 30

    if _keywords_match(keywords, _LIGHT_KEYWORD_TRIGGERS):
        score += 20

    return _clamp(score)


def _score_workout(genres: list[str]) -> int:
    score = _BASE_SCORE

    if any(genre in _ACTIVE_GENRES for genre in genres):
        score += 25

    if any(genre in _LOW_DIALOGUE_GENRES for genre in genres):
        score += 15

    return _clamp(score)


def _score_before_sleep(genres: list[str], sentiment_score: dict, keywords: list[str]) -> int:
    score = _BASE_SCORE

    score += sentiment_score.get("score", 0) * 15

    if sentiment_score.get("label") == "긍정":
        score += 10

    if _keywords_match(keywords, _CALM_KEYWORD_TRIGGERS):
        score += 20

    if any(genre in _INTENSE_GENRES for genre in genres):
        score -= 25

    return _clamp(score)


def calculate_fit_scores(movie: dict, all_movies: list[dict]) -> dict:
    genres = movie.get("genre", [])
    keywords = movie.get("keywords", [])
    sentiment_score = movie.get("sentiment_score", {})

    effective_runtime = _effective_runtime(movie)
    threshold = _short_runtime_threshold(all_movies)

    return {
        "식사시간": _score_mealtime(effective_runtime, threshold, keywords),
        "운동중": _score_workout(genres),
        "자기전": _score_before_sleep(genres, sentiment_score, keywords),
    }
