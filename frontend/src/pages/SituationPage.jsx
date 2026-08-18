import { useEffect, useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { getSituationContents } from '../api'
import { sentimentClass } from '../utils'

function SituationPage() {
  const { situationName } = useParams()
  const navigate = useNavigate()
  const [contents, setContents] = useState([])
  const [status, setStatus] = useState('loading')

  useEffect(() => {
    let cancelled = false

    setStatus('loading')
    getSituationContents(situationName)
      .then((data) => {
        if (cancelled) return
        setContents(data)
        setStatus('done')
      })
      .catch(() => {
        if (!cancelled) setStatus('error')
      })

    return () => {
      cancelled = true
    }
  }, [situationName])

  return (
    <div className="page">
      <button type="button" className="back-button" onClick={() => navigate('/')}>
        ← 돌아가기
      </button>
      <h1>{situationName}</h1>

      {status === 'loading' && <p className="message">불러오는 중...</p>}
      {status === 'error' && <p className="message error">콘텐츠를 불러오지 못했습니다.</p>}
      {status === 'done' && contents.length === 0 && (
        <p className="message">추천할 콘텐츠가 없습니다.</p>
      )}

      <div className="card-grid">
        {contents.map((content) => (
          <Link key={content.id} to={`/contents/${content.id}`} className="content-card">
            <div className="content-card-poster">
              {content.poster_url && <img src={content.poster_url} alt={content.title} />}
            </div>
            <div className="content-card-body">
              <h2 className="content-card-title">{content.title}</h2>
              <span className="fit-score-badge">적합도 {content.fit_score}</span>
              <div className="tag-list">
                {content.keywords?.map((keyword) => (
                  <span key={keyword} className="tag">
                    #{keyword}
                  </span>
                ))}
              </div>
              {content.sentiment_label && (
                <span className={`sentiment-badge sentiment-${sentimentClass(content.sentiment_label)}`}>
                  {content.sentiment_label}
                </span>
              )}
            </div>
          </Link>
        ))}
      </div>
    </div>
  )
}

export default SituationPage
