import json
import os
import re

from konlpy.tag import Okt
from sklearn.feature_extraction.text import TfidfVectorizer

_LEXICON_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "SentiWord_info.json")

_OKT = Okt()

_STOPWORDS = [
    "영화", "리뷰", "후기", "이번", "정말", "정도", "그냥", "너무", "진짜",
    "생각", "사람", "부분", "이야기", "장면", "느낌", "완전", "그리고",
    "하지만", "그런데", "이런", "저런", "때문", "이제", "우리", "자신",
]


def _load_lexicon() -> dict[str, int]:
    with open(_LEXICON_PATH, encoding="utf-8") as f:
        entries = json.load(f)

    lexicon: dict[str, int] = {}
    for entry in entries:
        word = entry.get("word", "").strip()
        if len(word) < 2:
            continue
        try:
            lexicon[word] = int(entry.get("polarity", "0"))
        except ValueError:
            lexicon[word] = 0

    return lexicon


_LEXICON = _load_lexicon()
_LEXICON_WORDS = sorted(_LEXICON, key=len, reverse=True)


def _flush_noun_run(run: list[str], tokens: list[str]) -> None:
    if not run:
        return
    merged = "".join(run)
    if len(merged) >= 2 and merged not in _STOPWORDS:
        tokens.append(merged)


def _tokenize(text: str) -> list[str]:
    # Okt's dictionary sometimes splits a single loanword/compound (e.g.
    # "브레이킹" -> "브레이" + "킹") into multiple Noun tokens. Re-joining
    # nouns that are directly adjacent in the original text (no whitespace
    # between them) recovers the original term without merging across
    # separate words. A single pos() call on the whole text is used instead
    # of one call per word, since per-word calls are far too slow (JVM
    # round-trip cost per call) for a text with many words.
    tokens: list[str] = []
    current_run: list[str] = []
    cursor = 0

    for word, tag in _OKT.pos(text):
        idx = text.find(word, cursor)
        adjacent = idx != -1 and idx == cursor
        cursor = idx + len(word) if idx != -1 else cursor

        if tag == "Noun" and (adjacent or not current_run):
            current_run.append(word)
        else:
            _flush_noun_run(current_run, tokens)
            current_run = [word] if tag == "Noun" else []

    _flush_noun_run(current_run, tokens)

    return tokens


def analyze_sentiment(reviews: list[str]) -> dict:
    review_scores = []

    for review in reviews:
        matched_polarities = [_LEXICON[word] for word in _LEXICON_WORDS if word in review]
        if matched_polarities:
            review_scores.append(sum(matched_polarities) / len(matched_polarities))

    average_score = sum(review_scores) / len(review_scores) if review_scores else 0.0

    if average_score > 0.2:
        label = "긍정"
    elif average_score < -0.2:
        label = "부정"
    else:
        label = "중립"

    return {"score": round(average_score, 3), "label": label}


_STAR_RATING_THRESHOLDS = [
    (1.2, 5),
    (0.4, 4),
    (-0.4, 3),
    (-1.2, 2),
]


def convert_to_star_rating(sentiment_score: dict) -> int:
    score = sentiment_score.get("score", 0)

    for threshold, rating in _STAR_RATING_THRESHOLDS:
        if score >= threshold:
            return rating

    return 1


def analyze_sentiment_per_review(review_text: str) -> dict:
    sentiment_score = analyze_sentiment([review_text])
    star_rating = convert_to_star_rating(sentiment_score)
    return {**sentiment_score, "star_rating": star_rating}


_HASHTAG_RE = re.compile(r"#\S+")
_SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?\n])\s+")
_ZERO_WIDTH_RE = re.compile("[​﻿]")
_WHITESPACE_RE = re.compile(r"\s+")

_OPINION_KEYWORDS = [
    "좋았다", "별로", "추천", "몰입", "재밌", "지루", "실망",
    "인생영화", "꿀잼", "노잼", "아쉽", "만족",
]

_AD_WIDGET_TOKENS = ["728x90", "반응형", "LIST", "SMALL"]
_CCL_PHRASES = ["저작자표시", "비영리", "변경금지", "(새창열림)"]
_TRAILING_SECTION_MARKERS = ["카테고리의 다른 글", "관련글", "태그"]
_BUSINESS_INFO_MARKERS = ["사업자 정보 표시", "사업자 등록번호", "통신판매신고번호"]

_AD_WIDGET_RE = re.compile("|".join(re.escape(token) for token in _AD_WIDGET_TOKENS))
_CCL_RE = re.compile("|".join(re.escape(phrase) for phrase in _CCL_PHRASES))
_DATE_LIST_ITEM_RE = re.compile(r"\(\d+\)\s*\d{4}\.\d{2}\.\d{2}")

_RELEVANCE_MIN_MENTIONS = 1
_MAX_SNIPPET_TOTAL_LENGTH = 280
_MIN_SHORT_TITLE_LENGTH = 5
_GENERIC_FRANCHISE_WORDS = {"스파이더맨", "마블", "디즈니", "픽사", "DC"}


def _title_candidates(content_title: str) -> list[str]:
    candidates = [content_title]

    # TV titles often carry a season/subtitle after a colon (e.g. "브레이킹
    # 배드: 시즌1"); the part before the colon is usually how the series is
    # actually referred to in blog posts. But a short_title that's too short
    # or a bare franchise name ("스파이더맨", "마블") matches far too many
    # unrelated posts, so those fall back to requiring the full title.
    short_title = content_title.split(":")[0].strip()
    if (
        short_title
        and short_title != content_title
        and len(short_title) >= _MIN_SHORT_TITLE_LENGTH
        and short_title not in _GENERIC_FRANCHISE_WORDS
    ):
        candidates.append(short_title)

    return candidates


def _strip_boilerplate(full_text: str) -> str:
    text = full_text

    cutoff_positions = [pos for pos in (text.find(marker) for marker in _TRAILING_SECTION_MARKERS) if pos != -1]
    if cutoff_positions:
        text = text[: min(cutoff_positions)]

    kept_paragraphs = [
        paragraph
        for paragraph in text.split("\n")
        if not any(marker in paragraph for marker in _BUSINESS_INFO_MARKERS)
        and not _DATE_LIST_ITEM_RE.search(paragraph)
    ]
    text = "\n".join(kept_paragraphs)

    text = _AD_WIDGET_RE.sub("", text)
    text = _CCL_RE.sub("", text)

    return text


def extract_opinion_sentences(
    full_text: str, content_title: str = "", max_sentences: int = 2
) -> list[str]:
    if not full_text:
        return []

    cleaned_text = _strip_boilerplate(full_text)

    if content_title:
        candidates = _title_candidates(content_title)
        mention_count = max(cleaned_text.count(candidate) for candidate in candidates)
        if mention_count < _RELEVANCE_MIN_MENTIONS:
            return []

    without_hashtags = _HASHTAG_RE.sub("", cleaned_text)
    raw_sentences = _SENTENCE_SPLIT_RE.split(without_hashtags)
    sentences = [
        _WHITESPACE_RE.sub(" ", _ZERO_WIDTH_RE.sub("", s)).strip() for s in raw_sentences
    ]
    sentences = [s for s in sentences if s]

    opinion_sentences = [
        sentence
        for sentence in sentences
        if any(keyword in sentence for keyword in _OPINION_KEYWORDS)
    ]

    selected: list[str] = []
    total_length = 0
    for sentence in opinion_sentences:
        if len(selected) >= max_sentences:
            break
        extra_length = len(sentence) + (1 if selected else 0)
        if total_length + extra_length > _MAX_SNIPPET_TOTAL_LENGTH:
            break
        selected.append(sentence)
        total_length += extra_length

    return selected


def extract_keywords(reviews: list[str], top_n: int = 5) -> list[str]:
    if not reviews:
        return []

    vectorizer = TfidfVectorizer(tokenizer=_tokenize, token_pattern=None, stop_words=_STOPWORDS)

    try:
        tfidf_matrix = vectorizer.fit_transform(reviews)
    except ValueError:
        return []

    scores = tfidf_matrix.sum(axis=0).A1
    terms = vectorizer.get_feature_names_out()

    ranked = sorted(zip(terms, scores), key=lambda pair: pair[1], reverse=True)
    return [term for term, _ in ranked if len(term) >= 2][:top_n]
