import json
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = "gpt-4o-mini"

_MAX_INPUT_CHARS = 4000
_MAX_SUMMARY_LENGTH = 280

_SYSTEM_PROMPT = """당신은 영화/TV 리뷰 블로그 글을 분석하는 어시스턴트입니다.
주어진 블로그 본문이 특정 작품에 대한 실제 감상평인지 판단하세요.

아래와 같은 글은 관련없음(is_relevant: false)으로 판단하세요:
- 광고, 협찬 문구가 주가 되는 글
- 다른 사이트/서비스로의 홍보 링크가 주 내용인 글
- 영화관/상영관 추천(예: "IMAX로 보세요"), 좌석 후기 등 관람 환경 안내가 주가 되는 글
- 방송 편성표, 상영 시간표 안내
- 티켓 예매 방법 안내

실제 감상평(줄거리 감상, 연출/연기/재미에 대한 평가 등)이면 is_relevant를 true로 하고:
- 영화 내용 자체에 대한 감상만 뽑아 2문장 이내(280자 이하)로 한국어로 요약
- 감상 톤을 바탕으로 1~5점 사이의 정수 별점을 부여 (1=매우 부정적, 5=매우 긍정적)

반드시 아래 JSON 형식으로만 응답하세요:
{"is_relevant": true 또는 false, "summary": "..." 또는 null, "star_rating": 1~5 정수 또는 null}
"""

_EMPTY_RESULT = {"is_relevant": False, "summary": None, "star_rating": None}

_client: OpenAI | None = None


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(api_key=OPENAI_API_KEY)
    return _client


def process_review_with_llm(full_text: str, movie_title: str) -> dict:
    if not full_text or not full_text.strip():
        return dict(_EMPTY_RESULT)

    client = _get_client()

    try:
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            response_format={"type": "json_object"},
            temperature=0.3,
            messages=[
                {"role": "system", "content": _SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": f"작품 제목: {movie_title}\n\n블로그 본문:\n{full_text[:_MAX_INPUT_CHARS]}",
                },
            ],
        )
        result = json.loads(response.choices[0].message.content)
    except Exception:
        return dict(_EMPTY_RESULT)

    if not result.get("is_relevant"):
        return dict(_EMPTY_RESULT)

    summary = result.get("summary")
    summary = summary.strip()[:_MAX_SUMMARY_LENGTH] if isinstance(summary, str) else None
    if not summary:
        return dict(_EMPTY_RESULT)

    star_rating = result.get("star_rating")
    star_rating = max(1, min(5, round(star_rating))) if isinstance(star_rating, (int, float)) else None

    return {"is_relevant": True, "summary": summary, "star_rating": star_rating}
