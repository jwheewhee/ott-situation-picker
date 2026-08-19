import { useNavigate } from 'react-router-dom'
import { PopcornMascot } from '../components/Mascots'

const SITUATIONS = ['식사시간', '운동중', '자기전']

function HomePage() {
  const navigate = useNavigate()

  return (
    <div className="page home-page">
      <div className="home-mascot">
        <PopcornMascot size={320} />
      </div>
      <h1>지금 뭐 볼까?</h1>
      <p className="subtitle">상황을 선택하면 딱 맞는 콘텐츠를 추천해드려요.</p>

      <div className="situation-buttons">
        {SITUATIONS.map((situation) => (
          <button
            key={situation}
            type="button"
            className="situation-button"
            onClick={() => navigate(`/situations/${encodeURIComponent(situation)}`)}
          >
            {situation}
          </button>
        ))}
      </div>
    </div>
  )
}

export default HomePage
