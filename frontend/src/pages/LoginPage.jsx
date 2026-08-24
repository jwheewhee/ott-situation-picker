import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { supabase } from '../supabaseClient'

function LoginPage() {
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const [formError, setFormError] = useState(null)

  async function handleSubmit(event) {
    event.preventDefault()
    setSubmitting(true)
    setFormError(null)

    const { error } = await supabase.auth.signInWithPassword({
      email: email.trim(),
      password,
    })

    if (error) {
      setFormError('이메일 또는 비밀번호가 올바르지 않아요.')
      setSubmitting(false)
      return
    }

    navigate('/')
  }

  return (
    <div className="auth-page">
      <Link to="/" className="site-logo">
        FlixFit
      </Link>

      <form className="auth-form" onSubmit={handleSubmit}>
        <h1>로그인</h1>

        <input
          type="email"
          placeholder="이메일"
          value={email}
          onChange={(event) => setEmail(event.target.value)}
          required
          autoComplete="email"
          className="auth-input"
        />
        <input
          type="password"
          placeholder="비밀번호"
          value={password}
          onChange={(event) => setPassword(event.target.value)}
          required
          autoComplete="current-password"
          className="auth-input"
        />

        {formError && <p className="user-review-error">{formError}</p>}

        <button type="submit" className="auth-submit" disabled={submitting}>
          {submitting ? '로그인 중...' : '로그인'}
        </button>

        <p className="auth-switch-link">
          계정이 없으신가요? <Link to="/signup">회원가입</Link>
        </p>
      </form>
    </div>
  )
}

export default LoginPage
