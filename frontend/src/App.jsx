import { Route, Routes } from 'react-router-dom'
import HomePage from './pages/HomePage'
import SituationPage from './pages/SituationPage'
import ContentDetailPage from './pages/ContentDetailPage'

function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/situations/:situationName" element={<SituationPage />} />
      <Route path="/contents/:id" element={<ContentDetailPage />} />
    </Routes>
  )
}

export default App
