import html
import os
import re
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")
NAVER_BLOG_SEARCH_URL = "https://openapi.naver.com/v1/search/blog.json"

_TAG_RE = re.compile(r"<[^>]+>")

_IRRELEVANT_KEYWORDS = ["방탈출", "카페", "체험", "리마스터링"]

_QUERY_SUFFIXES = ["영화 후기", "리뷰"]


def _clean_text(text: str) -> str:
    return html.unescape(_TAG_RE.sub("", text)).strip()


def _is_relevant(item: dict) -> bool:
    text = f"{item['title']} {item['description']}"
    return not any(keyword in text for keyword in _IRRELEVANT_KEYWORDS)


def _search_naver_blog_once(query: str, count: int) -> list[dict]:
    response = requests.get(
        NAVER_BLOG_SEARCH_URL,
        headers={
            "X-Naver-Client-Id": NAVER_CLIENT_ID,
            "X-Naver-Client-Secret": NAVER_CLIENT_SECRET,
        },
        params={
            "query": query,
            "display": count,
            "sort": "sim",
        },
        timeout=10,
    )
    response.raise_for_status()
    items = response.json().get("items", [])

    return [
        {
            "title": _clean_text(item.get("title", "")),
            "description": _clean_text(item.get("description", "")),
            "link": item.get("link", ""),
        }
        for item in items
    ]


def search_naver_blog(movie_title: str, count: int = 10) -> list[dict]:
    all_items: list[dict] = []
    for suffix in _QUERY_SUFFIXES:
        all_items.extend(_search_naver_blog_once(f"{movie_title} {suffix}", count))

    seen_links: set[str] = set()
    deduped_items = []
    for item in all_items:
        link = item["link"]
        if link and link in seen_links:
            continue
        if link:
            seen_links.add(link)
        deduped_items.append(item)

    return [item for item in deduped_items if _is_relevant(item)]


_REQUEST_HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

_NAVER_CONTENT_SELECTORS = [".se-main-container", "#postViewArea"]


def _fetch_html(url: str) -> BeautifulSoup | None:
    try:
        response = requests.get(url, headers=_REQUEST_HEADERS, timeout=10)
        response.raise_for_status()
    except requests.RequestException:
        return None

    return BeautifulSoup(response.text, "html.parser")


def fetch_blog_full_text(url: str) -> str:
    if not url:
        return ""

    soup = _fetch_html(url)
    if soup is None:
        return ""

    is_naver_blog = "blog.naver.com" in url

    if is_naver_blog:
        # blog.naver.com renders the post inside an iframe; the real content
        # lives at the iframe's src, not the outer page.
        iframe = soup.find("iframe", id="mainFrame")
        if iframe and iframe.get("src"):
            inner_url = urljoin("https://blog.naver.com", iframe["src"])
            inner_soup = _fetch_html(inner_url)
            if inner_soup is not None:
                soup = inner_soup

        for selector in _NAVER_CONTENT_SELECTORS:
            content = soup.select_one(selector)
            if content:
                return content.get_text(separator="\n", strip=True)

        return ""

    # Best-effort fallback for non-Naver blog platforms (e.g. Tistory).
    article = soup.find("article")
    if article:
        return article.get_text(separator="\n", strip=True)

    paragraphs = soup.find_all("p")
    if paragraphs:
        return "\n".join(p.get_text(separator=" ", strip=True) for p in paragraphs)

    return ""
