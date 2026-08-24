import { useEffect, useRef, useState } from 'react'
import { Link, Outlet, useNavigate } from 'react-router-dom'
import { updateProfile } from '../api'
import { useAuth } from '../AuthContext'
import { AvatarIcon } from './AvatarPicker'
import { supabase } from '../supabaseClient'

function Layout() {
  const navigate = useNavigate()
  const { session, profile, setProfile } = useAuth()
  const [menuOpen, setMenuOpen] = useState(false)
  const [editingNickname, setEditingNickname] = useState(false)
  const [nicknameInput, setNicknameInput] = useState('')
  const [nicknameError, setNicknameError] = useState(null)
  const [savingNickname, setSavingNickname] = useState(false)
  const menuRef = useRef(null)

  useEffect(() => {
    if (!menuOpen) return

    function handleClickOutside(event) {
      if (menuRef.current && !menuRef.current.contains(event.target)) {
        setMenuOpen(false)
      }
    }

    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [menuOpen])

  useEffect(() => {
    if (!menuOpen) {
      setEditingNickname(false)
      setNicknameError(null)
    }
  }, [menuOpen])

  async function handleLogout() {
    setMenuOpen(false)
    await supabase.auth.signOut()
    navigate('/login')
  }

  function startEditingNickname() {
    setNicknameInput(profile?.nickname ?? '')
    setNicknameError(null)
    setEditingNickname(true)
  }

  async function handleNicknameSave(event) {
    event.preventDefault()
    const trimmed = nicknameInput.trim()
    if (!trimmed) return

    setSavingNickname(true)
    setNicknameError(null)

    try {
      const updated = await updateProfile({ nickname: trimmed })
      setProfile((prev) => ({ ...prev, nickname: updated.nickname }))
      setEditingNickname(false)
      setMenuOpen(false)
    } catch (err) {
      setNicknameError(err?.status === 409 ? '이미 사용중인 닉네임입니다.' : '닉네임 변경에 실패했어요.')
    } finally {
      setSavingNickname(false)
    }
  }

  return (
    <>
      <header className="site-header">
        <Link to="/" className="site-logo">
          FlixFit
        </Link>

        {session && (
          <div className="user-menu" ref={menuRef}>
            <button
              type="button"
              className="user-menu-trigger"
              onClick={() => setMenuOpen((prev) => !prev)}
              aria-expanded={menuOpen}
            >
              <AvatarIcon avatarId={profile?.avatar_id} size={32} />
              <span className="user-menu-nickname">{profile?.nickname ?? ''}</span>
            </button>

            {menuOpen && (
              <div className="user-menu-dropdown">
                {editingNickname ? (
                  <form className="nickname-edit-form" onSubmit={handleNicknameSave}>
                    <input
                      type="text"
                      className="nickname-edit-input"
                      value={nicknameInput}
                      onChange={(event) => setNicknameInput(event.target.value)}
                      maxLength={30}
                      autoFocus
                    />
                    {nicknameError && <p className="nickname-edit-error">{nicknameError}</p>}
                    <div className="nickname-edit-actions">
                      <button type="submit" className="nickname-edit-save" disabled={savingNickname}>
                        {savingNickname ? '저장 중...' : '저장'}
                      </button>
                      <button
                        type="button"
                        className="nickname-edit-cancel"
                        onClick={() => setEditingNickname(false)}
                      >
                        취소
                      </button>
                    </div>
                  </form>
                ) : (
                  <>
                    <Link to="/my" className="user-menu-link" onClick={() => setMenuOpen(false)}>
                      내 리뷰 보기
                    </Link>
                    <button type="button" className="user-menu-link" onClick={startEditingNickname}>
                      닉네임 수정
                    </button>
                    <button type="button" className="user-menu-logout" onClick={handleLogout}>
                      로그아웃
                    </button>
                  </>
                )}
              </div>
            )}
          </div>
        )}
      </header>
      <Outlet />
    </>
  )
}

export default Layout
