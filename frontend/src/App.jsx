import { useState } from 'react'
import { Navigate, Outlet, Route, Routes } from 'react-router-dom'
import { AuthProvider, useAuth } from './AuthContext'
import Layout from './components/Layout'
import SplashScreen from './components/SplashScreen'
import HomePage from './pages/HomePage'
import LoginPage from './pages/LoginPage'
import MyPage from './pages/MyPage'
import SignupPage from './pages/SignupPage'
import SituationPage from './pages/SituationPage'
import ContentDetailPage from './pages/ContentDetailPage'

const SPLASH_SESSION_KEY = 'flixfit_splash_shown'

function ProtectedRoute() {
  const { session, loading } = useAuth()

  if (loading) {
    return (
      <div className="page">
        <p className="message">불러오는 중...</p>
      </div>
    )
  }

  if (!session) {
    return <Navigate to="/login" replace />
  }

  return <Outlet />
}

function App() {
  const [showSplash, setShowSplash] = useState(
    () => !sessionStorage.getItem(SPLASH_SESSION_KEY)
  )

  function handleSplashFinish() {
    sessionStorage.setItem(SPLASH_SESSION_KEY, 'true')
    setShowSplash(false)
  }

  return (
    <AuthProvider>
      {showSplash && <SplashScreen onFinish={handleSplashFinish} />}
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/signup" element={<SignupPage />} />
        <Route element={<ProtectedRoute />}>
          <Route element={<Layout />}>
            <Route path="/" element={<HomePage />} />
            <Route path="/my" element={<MyPage />} />
            <Route path="/situations/:situationName" element={<SituationPage />} />
            <Route path="/contents/:id" element={<ContentDetailPage />} />
          </Route>
        </Route>
      </Routes>
    </AuthProvider>
  )
}

export default App
