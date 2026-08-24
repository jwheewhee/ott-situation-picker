import os

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from postgrest.exceptions import APIError
from pydantic import BaseModel, Field

from app.auth import get_current_user_id
from app.db import supabase
from app.services.analysis import analyze_sentiment, extract_keywords
from app.services.naver import search_naver_blog
from app.services.netflix_top10 import get_netflix_top10_titles
from app.services.scoring import calculate_fit_scores
from app.services.storage import save_to_db
from app.services.tmdb import get_metadata_for_titles, get_netflix_movies, get_netflix_tv

load_dotenv()

ALLOWED_ORIGIN = os.getenv("ALLOWED_ORIGIN", "http://localhost:5177")

app = FastAPI(title="OTT Situation Picker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
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
    top10_contents = get_metadata_for_titles(get_netflix_top10_titles())
    top10_titles = {content["title"] for content in top10_contents}

    discover_contents = get_netflix_movies(count=30) + get_netflix_tv(count=30)
    deduped_discover = [
        content for content in discover_contents if content["title"] not in top10_titles
    ]

    contents = top10_contents + deduped_discover

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
    content_ids: list[int], limit_per_content: int = 3
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


def _fetch_content_ids_with_reviews(content_ids: list[int]) -> set[int]:
    if not content_ids:
        return set()

    rows = supabase.table("review").select("content_id").in_("content_id", content_ids).execute().data
    return {row["content_id"] for row in rows}


def _fetch_profiles_by_user_ids(user_ids: list[str]) -> dict[str, int]:
    if not user_ids:
        return {}

    rows = supabase.table("profiles").select("id, avatar_id").in_("id", user_ids).execute().data
    return {row["id"]: row["avatar_id"] for row in rows}


def _fetch_review_snippets_with_rating(content_id: int) -> list[dict]:
    rows = (
        supabase.table("review")
        .select("description, summary, star_rating")
        .eq("content_id", content_id)
        .execute()
        .data
    )
    return [
        {"summary": row["summary"] or row["description"], "star_rating": row["star_rating"]}
        for row in rows
        if row["summary"] or row["description"]
    ]


@app.get("/api/situations/{situation_name}/contents")
def get_situation_contents(situation_name: str):
    situation = _execute_maybe_single(supabase.table("situation").select("id").eq("name", situation_name))
    if situation is None:
        raise HTTPException(status_code=404, detail="situation not found")

    rows = (
        supabase.table("content_situation")
        .select("fit_score, content(id, title, genre, poster_url, runtime, star_rating)")
        .eq("situation_id", situation["id"])
        .gte("fit_score", 60)
        .order("fit_score", desc=True)
        .execute()
        .data
    )

    content_ids = [row["content"]["id"] for row in rows if row["content"]]
    tags_by_content_id = _fetch_review_tags_by_content_id(content_ids)
    snippets_by_content_id = _fetch_review_snippets_by_content_id(content_ids)
    content_ids_with_reviews = _fetch_content_ids_with_reviews(content_ids)

    results = []
    for row in rows:
        content = row["content"]
        if content is None:
            continue
        if not content.get("poster_url"):
            continue
        if content["id"] not in content_ids_with_reviews:
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

    user_reviews = (
        supabase.table("user_review")
        .select("nickname, review_text, star_rating, created_at, user_id")
        .eq("content_id", content_id)
        .order("created_at", desc=True)
        .execute()
        .data
    )

    avatar_by_user_id = _fetch_profiles_by_user_ids(
        [row["user_id"] for row in user_reviews if row["user_id"]]
    )
    for row in user_reviews:
        row["avatar_id"] = avatar_by_user_id.get(row["user_id"])

    return {
        **content,
        "review_tags": review_tags,
        "fit_scores": fit_scores,
        "review_snippets": review_snippets,
        "user_reviews": user_reviews,
    }


class UserReviewCreate(BaseModel):
    review_text: str = Field(min_length=5)
    star_rating: int = Field(ge=1, le=5)


@app.post("/api/contents/{content_id}/reviews")
def create_user_review(
    content_id: int,
    payload: UserReviewCreate,
    user_id: str = Depends(get_current_user_id),
):
    content = _execute_maybe_single(supabase.table("content").select("id").eq("id", content_id))
    if content is None:
        raise HTTPException(status_code=404, detail="content not found")

    profile = _execute_maybe_single(
        supabase.table("profiles").select("nickname, avatar_id").eq("id", user_id)
    )
    if profile is None:
        raise HTTPException(status_code=404, detail="profile not found")

    row = {
        "content_id": content_id,
        "user_id": user_id,
        "nickname": profile["nickname"],
        "review_text": payload.review_text,
        "star_rating": payload.star_rating,
    }

    result = supabase.table("user_review").insert(row).execute()
    return {**result.data[0], "avatar_id": profile["avatar_id"]}


@app.get("/api/my/reviews")
def get_my_reviews(user_id: str = Depends(get_current_user_id)):
    rows = (
        supabase.table("user_review")
        .select("id, content_id, review_text, star_rating, created_at, content(title, poster_url)")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .execute()
        .data
    )
    return rows


class ProfileUpdate(BaseModel):
    nickname: str = Field(min_length=1, max_length=30)


@app.patch("/api/profile")
def update_profile(payload: ProfileUpdate, user_id: str = Depends(get_current_user_id)):
    try:
        result = (
            supabase.table("profiles")
            .update({"nickname": payload.nickname.strip()})
            .eq("id", user_id)
            .execute()
        )
    except APIError as exc:
        if exc.code == "23505":
            raise HTTPException(status_code=409, detail="이미 사용중인 닉네임입니다.") from None
        raise

    if not result.data:
        raise HTTPException(status_code=404, detail="profile not found")

    return result.data[0]
