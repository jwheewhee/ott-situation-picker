import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { createUserReview, getContentDetail } from '../api'
import { formatDate, renderStars, sentimentClass } from '../utils'

const MIN_REVIEW_TEXT_LENGTH = 5

function StarPicker({ value, onChange }) {
  return (
    <div className="star-picker" role="radiogroup" aria-label="별점 선택">
      {[1, 2, 3, 4, 5].map((star) => (
        <button
          key={star}
          type="button"
          className="star-picker-star"
          aria-label={`${star}점`}
          aria-pressed={value >= star}
          onClick={() => onChange(star)}
        >
          {value >= star ? '★' : '☆'}
        </button>
      ))}
    </div>
  )
}

function UserReviewForm({ contentId, onCreated }) {
  const [nickname, setNickname] = useState('')
  const [starRating, setStarRating] = useState(0)
  const [reviewText, setReviewText] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const [formError, setFormError] = useState(null)

  const isTextValid = reviewText.trim().length >= MIN_REVIEW_TEXT_LENGTH
  const isRatingValid = starRating >= 1
  const canSubmit = isTextValid && isRatingValid && !submitting

  async function handleSubmit(event) {
    event.preventDefault()
    if (!canSubmit) return

    setSubmitting(true)
    setFormError(null)

    try {
      const newReview = await createUserReview(contentId, {
        nickname: nickname.trim() || undefined,
        review_text: reviewText.trim(),
        star_rating: starRating,
      })
      onCreated(newReview)
      setNickname('')
      setStarRating(0)
      setReviewText('')
    } catch {
      setFormError('리뷰 등록에 실패했어요. 잠시 후 다시 시도해주세요.')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <form className="user-review-form" onSubmit={handleSubmit}>
      <input
        type="text"
        className="user-review-nickname-input"
        placeholder="익명"
        value={nickname}
        onChange={(event) => setNickname(event.target.value)}
        maxLength={30}
      />

      <StarPicker value={starRating} onChange={setStarRating} />

      <textarea
        className="user-review-textarea"
        placeholder="이 작품에 대한 감상을 남겨주세요 (최소 5자)"
        value={reviewText}
        onChange={(event) => setReviewText(event.target.value)}
        rows={3}
      />
      <p className="user-review-hint">
        최소 {MIN_REVIEW_TEXT_LENGTH}자 이상 입력해주세요. ({reviewText.trim().length}자)
      </p>

      {formError && <p className="user-review-error">{formError}</p>}

      <button type="submit" className="user-review-submit" disabled={!canSubmit}>
        {submitting ? '등록 중...' : '등록'}
      </button>
    </form>
  )
}

function ContentDetailPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [content, setContent] = useState(null)
  const [userReviews, setUserReviews] = useState([])
  const [status, setStatus] = useState('loading')

  useEffect(() => {
    let cancelled = false

    setStatus('loading')
    getContentDetail(id)
      .then((data) => {
        if (cancelled) return
        setContent(data)
        setUserReviews(data.user_reviews ?? [])
        setStatus('done')
      })
      .catch(() => {
        if (!cancelled) setStatus('error')
      })

    return () => {
      cancelled = true
    }
  }, [id])

  if (status === 'loading') {
    return (
      <div className="page">
        <p className="message">불러오는 중...</p>
      </div>
    )
  }

  if (status === 'error' || !content) {
    return (
      <div className="page">
        <button type="button" className="back-button" onClick={() => navigate(-1)}>
          ← 뒤로
        </button>
        <p className="message error">콘텐츠를 불러오지 못했습니다.</p>
      </div>
    )
  }

  return (
    <div className="page">
      <button type="button" className="back-button" onClick={() => navigate(-1)}>
        ← 뒤로
      </button>

      <div className="detail-layout">
        <div className="detail-poster">
          {content.poster_url && <img src={content.poster_url} alt={content.title} />}
        </div>

        <div className="detail-body">
          <h1>{content.title}</h1>

          <div className="star-rating" aria-label={`평점 ${content.star_rating ?? '정보 없음'} / 5`}>
            {content.star_rating != null ? (
              <>
                <span className="star-rating-icons">{renderStars(content.star_rating)}</span>
                <span className="star-rating-value">{content.star_rating} / 5</span>
              </>
            ) : (
              <span className="star-rating-empty">평점 정보 없음</span>
            )}
          </div>

          <div className="tag-list">
            {content.genre?.map((genre) => (
              <span key={genre} className="tag">
                {genre}
              </span>
            ))}
          </div>

          <p className="runtime">
            러닝타임 {content.runtime != null ? `${content.runtime}분` : '정보 없음'}
          </p>

          <p className="overview">{content.overview}</p>

          <h2>상황별 적합도</h2>
          <div className="fit-score-list">
            {Object.entries(content.fit_scores ?? {}).map(([situationName, score]) => (
              <div key={situationName} className="fit-score-row">
                <span className="fit-score-name">{situationName}</span>
                <div className="fit-score-bar-track">
                  <div className="fit-score-bar-fill" style={{ width: `${score}%` }} />
                </div>
                <span className="fit-score-value">{score}</span>
              </div>
            ))}
          </div>

          <h2>리뷰 키워드</h2>
          <div className="tag-list">
            {content.review_tags?.map((tag, index) => (
              <span
                key={`${tag.tag_name}-${index}`}
                className={`tag sentiment-${sentimentClass(tag.sentiment_label)}`}
              >
                #{tag.tag_name}
              </span>
            ))}
            {content.review_tags?.length === 0 && (
              <span className="message">등록된 리뷰 키워드가 없습니다.</span>
            )}
          </div>
        </div>
      </div>

      <section className="review-section">
        <h2>블로그 후기</h2>
        {content.review_snippets?.length > 0 ? (
          <div className="review-quote-grid">
            {content.review_snippets.map((snippet, index) => (
              <blockquote key={index} className="review-quote-card">
                {snippet.star_rating != null && (
                  <span className="review-quote-rating">{renderStars(snippet.star_rating)}</span>
                )}
                <p className="review-quote-text">“{snippet.summary}”</p>
              </blockquote>
            ))}
          </div>
        ) : (
          <p className="empty-review-message">아직 등록된 후기가 없어요.</p>
        )}
      </section>

      <section className="review-section">
        <h2>시청자 리뷰</h2>

        <UserReviewForm
          contentId={id}
          onCreated={(newReview) => setUserReviews((prev) => [newReview, ...prev])}
        />

        {userReviews.length > 0 ? (
          <div className="user-review-grid">
            {userReviews.map((review, index) => (
              <div key={index} className="user-review-card">
                <div className="user-review-card-header">
                  <span className="user-review-nickname">{review.nickname}</span>
                  <span className="user-review-card-rating">{renderStars(review.star_rating)}</span>
                </div>
                <p className="user-review-text">{review.review_text}</p>
                <span className="user-review-date">{formatDate(review.created_at)}</span>
              </div>
            ))}
          </div>
        ) : (
          <p className="empty-review-message">아직 시청자 리뷰가 없어요. 첫 리뷰를 남겨보세요!</p>
        )}
      </section>
    </div>
  )
}

export default ContentDetailPage
