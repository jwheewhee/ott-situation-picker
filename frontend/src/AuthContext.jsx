import { createContext, useContext, useEffect, useState } from 'react'
import { supabase } from './supabaseClient'

const AuthContext = createContext(undefined)

export function AuthProvider({ children }) {
  const [session, setSession] = useState(null)
  const [profile, setProfile] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let cancelled = false

    supabase.auth.getSession().then(({ data }) => {
      if (cancelled) return
      setSession(data.session)
      setLoading(false)
    })

    const { data: listener } = supabase.auth.onAuthStateChange((_event, newSession) => {
      setSession(newSession)
    })

    return () => {
      cancelled = true
      listener.subscription.unsubscribe()
    }
  }, [])

  useEffect(() => {
    let cancelled = false
    const userId = session?.user?.id

    if (!userId) {
      setProfile(null)
      return
    }

    supabase
      .from('profiles')
      .select('nickname, avatar_id')
      .eq('id', userId)
      .maybeSingle()
      .then(({ data }) => {
        if (!cancelled) setProfile(data)
      })

    return () => {
      cancelled = true
    }
  }, [session?.user?.id])

  const value = {
    session,
    user: session?.user ?? null,
    profile,
    setProfile,
    loading,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
