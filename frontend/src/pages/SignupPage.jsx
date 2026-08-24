import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import AvatarPicker from '../components/AvatarPicker'
import { supabase } from '../supabaseClient'

const MIN_NICKNAME_LENGTH = 2
const MIN_PASSWORD_LENGTH = 6

function SignupPage() {
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [nickname, setNickname] = useState('')
  const [avatarId, setAvatarId] = useState(null)
  const [submitting, setSubmitting] = useState(false)
  const [formError, setFormError] = useState(null)

  const isEmailValid = email.trim().length > 0
  const isPasswordValid = password.length >= MIN_PASSWORD_LENGTH
  const isNicknameValid = nickname.trim().length >= MIN_NICKNAME_LENGTH
  const isAvatarValid = avatarId != null
  const canSubmit = isEmailValid && isPasswordValid && isNicknameValid && isAvatarValid && !submitting

  async function handleSubmit(event) {
    event.preventDefault()
    if (!canSubmit) return

    setSubmitting(true)
    setFormError(null)

    const { data, error } = await supabase.auth.signUp({
      email: email.trim(),
      password,
    })

    if (error) {
      setFormError(error.message || '회원가입에 실패했어요.')
      setSubmitting(false)
      return
    }

    const userId = data.user?.id
    if (!userId) {
      setFormError('회원가입에 실패했어요. 잠시 후 다시 시도해주세요.')
      setSubmitting(false)
      return
    }

    const { error: profileError } = await supabase
      .from('profiles')
      .insert({ id: userId, nickname: nickname.trim(), avatar_id: avatarId })

    if (profileError) {
      setFormError(
        data.session
          ? '프로필 생성에 실패했어요. 닉네임이 이미 사용 중일 수 있어요.'
          : '계정은 생성됐지만 프로필 등록에 실패했어요. 이메일 인증이 필요한 설정이라면 인증 후 다시 시도해주세요.'
      )
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
        <h1>회원가입</h1>

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
          placeholder={`비밀번호 (최소 ${MIN_PASSWORD_LENGTH}자)`}
          value={password}
          onChange={(event) => setPassword(event.target.value)}
          required
          minLength={MIN_PASSWORD_LENGTH}
          autoComplete="new-password"
          className="auth-input"
        />
        <input
          type="text"
          placeholder="닉네임"
          value={nickname}
          onChange={(event) => setNickname(event.target.value)}
          required
          maxLength={30}
          className="auth-input"
        />

        <p className="auth-avatar-label">아바타를 선택해주세요</p>
        <AvatarPicker value={avatarId} onChange={setAvatarId} />

        {formError && <p className="user-review-error">{formError}</p>}

        <button type="submit" className="auth-submit" disabled={!canSubmit}>
          {submitting ? '가입 중...' : '회원가입'}
        </button>

        <p className="auth-switch-link">
          이미 계정이 있으신가요? <Link to="/login">로그인</Link>
        </p>
      </form>
    </div>
  )
}

export default SignupPage
