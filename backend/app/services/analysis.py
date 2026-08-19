import json
import os

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
