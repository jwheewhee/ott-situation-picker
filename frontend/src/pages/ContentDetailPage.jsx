import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { getContentDetail } from '../api'
import { renderStars, sentimentClass } from '../utils'

function ContentDetailPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [content, setContent] = useState(null)
  const [status, setStatus] = useState('loading')

  useEffect(() => {
    let cancelled = false

    setStatus('loading')
    getContentDetail(id)
      .then((data) => {
        if (cancelled) return
        setContent(data)
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
        <h2>실제 이용자 후기</h2>
        {content.review_snippets?.length > 0 ? (
          <div className="review-quote-grid">
            {content.review_snippets.map((snippet, index) => (
              <blockquote key={index} className="review-quote-card">
                {snippet.star_rating != null && (
                  <span className="review-quote-rating">{renderStars(snippet.star_rating)}</span>
                )}
                <p className="review-quote-text">“{snippet.description}”</p>
              </blockquote>
            ))}
          </div>
        ) : (
          <p className="message">등록된 후기가 없습니다.</p>
        )}
      </section>
    </div>
  )
}

export default ContentDetailPage
