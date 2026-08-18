import html
import os
import re

import requests
from dotenv import load_dotenv

load_dotenv()

NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")
NAVER_BLOG_SEARCH_URL = "https://openapi.naver.com/v1/search/blog.json"

_TAG_RE = re.compile(r"<[^>]+>")

_IRRELEVANT_KEYWORDS = ["방탈출", "카페", "체험", "리마스터링"]


def _clean_text(text: str) -> str:
    return html.unescape(_TAG_RE.sub("", text)).strip()


def _is_relevant(item: dict) -> bool:
    text = f"{item['title']} {item['description']}"
    return not any(keyword in text for keyword in _IRRELEVANT_KEYWORDS)


def search_naver_blog(movie_title: str, count: int = 5) -> list[dict]:
    response = requests.get(
        NAVER_BLOG_SEARCH_URL,
        headers={
            "X-Naver-Client-Id": NAVER_CLIENT_ID,
            "X-Naver-Client-Secret": NAVER_CLIENT_SECRET,
        },
        params={
            "query": f"{movie_title} 영화 후기",
            "display": count,
            "sort": "sim",
        },
        timeout=10,
    )
    response.raise_for_status()
    items = response.json().get("items", [])

    cleaned_items = [
        {
            "title": _clean_text(item.get("title", "")),
            "description": _clean_text(item.get("description", "")),
        }
        for item in items
    ]

    return [item for item in cleaned_items if _is_relevant(item)]
