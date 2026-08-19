from app.db import supabase
from app.services.analysis import analyze_sentiment_per_review, convert_to_star_rating, extract_opinion_sentences
from app.services.naver import fetch_blog_full_text


def _effective_runtime(content: dict) -> int | None:
    runtime = content.get("runtime")
    if runtime is not None:
        return runtime
    return content.get("episode_run_time")


def _delete_stale_content(current_titles: set[str]) -> int:
    all_content = supabase.table("content").select("id, title").execute().data
    stale_ids = [row["id"] for row in all_content if row["title"] not in current_titles]

    if not stale_ids:
        return 0

    # Never delete content that a real person left a review on, even if it
    # dropped out of this sync's result set - user_review cascades on
    # content delete, and that data can't be recomputed like the scraped
    # review/review_tag rows can.
    reviewed_ids = {
        row["content_id"]
        for row in supabase.table("user_review")
        .select("content_id")
        .in_("content_id", stale_ids)
        .execute()
        .data
    }
    deletable_ids = [cid for cid in stale_ids if cid not in reviewed_ids]

    if deletable_ids:
        supabase.table("content").delete().in_("id", deletable_ids).execute()

    return len(deletable_ids)


def save_to_db(contents: list[dict]) -> dict:
    content_rows = [
        {
            "title": content["title"],
            "content_type": content["content_type"],
            "genre": content.get("genre", []),
            "runtime": _effective_runtime(content),
            "poster_url": content.get("poster_url"),
            "overview": content.get("overview"),
            "star_rating": convert_to_star_rating(content.get("sentiment_score", {})),
        }
        for content in contents
    ]

    upserted_content = (
        supabase.table("content").upsert(content_rows, on_conflict="title").execute().data
    )
    content_id_by_title = {row["title"]: row["id"] for row in upserted_content}

    contents_deleted = _delete_stale_content(set(content_id_by_title.keys()))

    situations = supabase.table("situation").select("id, name").execute().data
    situation_id_by_name = {row["name"]: row["id"] for row in situations}

    content_ids = list(content_id_by_title.values())
    if content_ids:
        supabase.table("review_tag").delete().in_("content_id", content_ids).execute()
        supabase.table("review").delete().in_("content_id", content_ids).execute()

    content_situation_rows = []
    review_tag_rows = []
    review_rows = []

    for content in contents:
        content_id = content_id_by_title.get(content["title"])
        if content_id is None:
            continue

        for situation_name, fit_score in content.get("fit_scores", {}).items():
            situation_id = situation_id_by_name.get(situation_name)
            if situation_id is None:
                continue
            content_situation_rows.append(
                {
                    "content_id": content_id,
                    "situation_id": situation_id,
                    "fit_score": fit_score,
                }
            )

        sentiment_score = content.get("sentiment_score", {})
        for keyword in content.get("keywords", []):
            review_tag_rows.append(
                {
                    "content_id": content_id,
                    "tag_name": keyword,
                    "sentiment_score": sentiment_score.get("score"),
                    "sentiment_label": sentiment_score.get("label"),
                }
            )

        for review in content.get("reviews", []):
            full_text = fetch_blog_full_text(review.get("link", ""))
            opinion_sentences = extract_opinion_sentences(full_text, content["title"])
            if not opinion_sentences:
                continue

            review_text = f"{review.get('title', '')} {review.get('description', '')}".strip()
            review_sentiment = analyze_sentiment_per_review(review_text)
            review_rows.append(
                {
                    "content_id": content_id,
                    "title": review.get("title"),
                    "description": review.get("description"),
                    "star_rating": review_sentiment["star_rating"],
                    "summary": " ".join(opinion_sentences),
                }
            )

    if content_situation_rows:
        supabase.table("content_situation").upsert(
            content_situation_rows, on_conflict="content_id,situation_id"
        ).execute()

    if review_tag_rows:
        supabase.table("review_tag").insert(review_tag_rows).execute()

    if review_rows:
        supabase.table("review").insert(review_rows).execute()

    return {
        "contents_saved": len(upserted_content),
        "contents_deleted": contents_deleted,
        "fit_scores_saved": len(content_situation_rows),
        "review_tags_saved": len(review_tag_rows),
        "reviews_saved": len(review_rows),
    }
