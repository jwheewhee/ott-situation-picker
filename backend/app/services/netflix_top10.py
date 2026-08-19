import io

import pandas as pd
import requests

NETFLIX_TOP10_URL = "https://www.netflix.com/tudum/top10/data/all-weeks-global.xlsx"

_CONTENT_TYPE_BY_CATEGORY_PREFIX = {
    "Films": "movie",
    "TV": "tv",
}


def _infer_content_type(category: str) -> str | None:
    for prefix, content_type in _CONTENT_TYPE_BY_CATEGORY_PREFIX.items():
        if category.startswith(prefix):
            return content_type
    return None


def get_netflix_top10_titles() -> list[dict]:
    response = requests.get(NETFLIX_TOP10_URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
    response.raise_for_status()

    df = pd.read_excel(io.BytesIO(response.content), sheet_name="Top 10")
    latest_week = df["week"].max()
    latest = df[df["week"] == latest_week].sort_values(["category", "weekly_rank"])

    titles = []
    for _, row in latest.iterrows():
        content_type = _infer_content_type(row["category"])
        if content_type is None:
            continue

        titles.append(
            {
                "title": row["show_title"],
                "content_type": content_type,
                "rank": int(row["weekly_rank"]),
                "week": latest_week,
            }
        )

    return titles
