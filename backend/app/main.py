from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.db import supabase
from app.services.analysis import analyze_sentiment, extract_keywords
from app.services.naver import search_naver_blog
from app.services.scoring import calculate_fit_scores
from app.services.storage import save_to_db
from app.services.tmdb import get_netflix_movies, get_netflix_tv

app = FastAPI(title="OTT Situation Picker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/api/contents")
def get_contents():
    return get_netflix_movies()


@app.get("/api/reviews")
def get_reviews(movie_title: str):
    return search_naver_blog(movie_title)


@app.get("/api/contents-with-reviews")
def get_contents_with_reviews():
    contents = get_netflix_movies() + get_netflix_tv()

    for content in contents:
        content["reviews"] = search_naver_blog(content["title"])

    return contents


@app.get("/api/contents-analyzed")
def get_contents_analyzed():
    movies = get_contents_with_reviews()

    for movie in movies:
        review_texts = [f"{r['title']} {r['description']}".strip() for r in movie["reviews"]]
        movie["sentiment_score"] = analyze_sentiment(review_texts)
        movie["keywords"] = extract_keywords(review_texts)

    return movies


@app.get("/api/contents-scored")
def get_contents_scored():
    movies = get_contents_analyzed()

    for movie in movies:
        movie["fit_scores"] = calculate_fit_scores(movie, movies)

    return movies


@app.post("/api/sync")
def sync_contents():
    contents = get_contents_scored()
    return save_to_db(contents)


def _execute_maybe_single(query):
    response = query.maybe_single().execute()
    return response.data if response is not None else None


def _fetch_review_tags_by_content_id(content_ids: list[int], limit_per_content: int = 5) -> dict[int, dict]:
    if not content_ids:
        return {}

    rows = (
        supabase.table("review_tag")
        .select("content_id, tag_name, sentiment_label")
        .in_("content_id", content_ids)
        .execute()
        .data
    )

    grouped: dict[int, dict] = {}
    for row in rows:
        bucket = grouped.setdefault(
            row["content_id"], {"keywords": [], "sentiment_label": row["sentiment_label"]}
        )
        if len(bucket["keywords"]) < limit_per_content:
            bucket["keywords"].append(row["tag_name"])

    return grouped


def _fetch_review_snippets_by_content_id(
    content_ids: list[int], limit_per_content: int = 5
) -> dict[int, list[str]]:
    if not content_ids:
        return {}

    rows = (
        supabase.table("review")
        .select("content_id, description")
        .in_("content_id", content_ids)
        .execute()
        .data
    )

    grouped: dict[int, list[str]] = {}
    for row in rows:
        if not row["description"]:
            continue
        snippets = grouped.setdefault(row["content_id"], [])
        if len(snippets) < limit_per_content:
            snippets.append(row["description"])

    return grouped


def _fetch_review_snippets_with_rating(content_id: int, limit: int = 5) -> list[dict]:
    rows = (
        supabase.table("review")
        .select("description, star_rating")
        .eq("content_id", content_id)
        .limit(limit)
        .execute()
        .data
    )
    return [row for row in rows if row["description"]]


@app.get("/api/situations/{situation_name}/contents")
def get_situation_contents(situation_name: str):
    situation = _execute_maybe_single(supabase.table("situation").select("id").eq("name", situation_name))
    if situation is None:
        raise HTTPException(status_code=404, detail="situation not found")

    rows = (
        supabase.table("content_situation")
        .select("fit_score, content(id, title, genre, poster_url, runtime, star_rating)")
        .eq("situation_id", situation["id"])
        .order("fit_score", desc=True)
        .execute()
        .data
    )

    content_ids = [row["content"]["id"] for row in rows if row["content"]]
    tags_by_content_id = _fetch_review_tags_by_content_id(content_ids)
    snippets_by_content_id = _fetch_review_snippets_by_content_id(content_ids)

    results = []
    for row in rows:
        content = row["content"]
        if content is None:
            continue

        tags = tags_by_content_id.get(content["id"], {"keywords": [], "sentiment_label": None})
        results.append(
            {
                **content,
                "fit_score": row["fit_score"],
                "keywords": tags["keywords"],
                "sentiment_label": tags["sentiment_label"],
                "review_snippets": snippets_by_content_id.get(content["id"], []),
            }
        )

    return results


@app.get("/api/contents/{content_id}")
def get_content_detail(content_id: int):
    content = _execute_maybe_single(supabase.table("content").select("*").eq("id", content_id))
    if content is None:
        raise HTTPException(status_code=404, detail="content not found")

    review_tags = (
        supabase.table("review_tag")
        .select("tag_name, sentiment_score, sentiment_label")
        .eq("content_id", content_id)
        .execute()
        .data
    )

    fit_score_rows = (
        supabase.table("content_situation")
        .select("fit_score, situation(name)")
        .eq("content_id", content_id)
        .execute()
        .data
    )
    fit_scores = {row["situation"]["name"]: row["fit_score"] for row in fit_score_rows if row["situation"]}

    review_snippets = _fetch_review_snippets_with_rating(content_id)

    return {
        **content,
        "review_tags": review_tags,
        "fit_scores": fit_scores,
        "review_snippets": review_snippets,
    }
