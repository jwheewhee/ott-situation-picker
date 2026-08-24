import { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { getMyReviews } from '../api'
import { SofaDogIcon } from '../components/Mascots'
import { formatDate, renderStars } from '../utils'

function MyPage() {
  const navigate = useNavigate()
  const [reviews, setReviews] = useState([])
  const [status, setStatus] = useState('loading')

  useEffect(() => {
    let cancelled = false

    setStatus('loading')
    getMyReviews()
      .then((data) => {
        if (cancelled) return
        setReviews(data)
        setStatus('done')
      })
      .catch(() => {
        if (!cancelled) setStatus('error')
      })

    return () => {
      cancelled = true
    }
  }, [])

  return (
    <div className="page">
      <button type="button" className="back-button" onClick={() => navigate('/')}>
        ← 돌아가기
      </button>
      <h1>내 리뷰</h1>

      {status === 'loading' && <p className="message">불러오는 중...</p>}
      {status === 'error' && <p className="message error">리뷰를 불러오지 못했습니다.</p>}

      {status === 'done' && reviews.length === 0 && (
        <div className="empty-reviews-mascot">
          <SofaDogIcon size={96} />
          <p>아직 남긴 리뷰가 없어요</p>
        </div>
      )}

      {status === 'done' && reviews.length > 0 && (
        <div className="my-review-grid">
          {reviews.map((review) => (
            <Link key={review.id} to={`/contents/${review.content_id}`} className="my-review-card">
              <div className="my-review-card-poster">
                {review.content?.poster_url && (
                  <img src={review.content.poster_url} alt={review.content.title} />
                )}
              </div>
              <div className="my-review-card-body">
                <h2 className="my-review-card-title">{review.content?.title}</h2>
                <span className="my-review-card-rating">{renderStars(review.star_rating)}</span>
                <p className="my-review-card-text">{review.review_text}</p>
                <span className="my-review-card-date">{formatDate(review.created_at)}</span>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  )
}

export default MyPage
