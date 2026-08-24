import { supabase } from './supabaseClient'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'

async function request(path, options) {
  const response = await fetch(`${API_BASE_URL}${path}`, options)
  if (!response.ok) {
    let detail = `Request failed: ${response.status}`
    try {
      const body = await response.json()
      if (body?.detail) detail = JSON.stringify(body.detail)
    } catch {
      // response had no JSON body; keep the generic message
    }
    const error = new Error(detail)
    error.status = response.status
    throw error
  }
  return response.json()
}

async function authorizedRequest(path, options = {}) {
  const { data } = await supabase.auth.getSession()
  const accessToken = data.session?.access_token

  return request(path, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(accessToken ? { Authorization: `Bearer ${accessToken}` } : {}),
      ...options.headers,
    },
  })
}

export function getSituationContents(situationName) {
  return request(`/api/situations/${encodeURIComponent(situationName)}/contents`)
}

export function getContentDetail(contentId) {
  return request(`/api/contents/${encodeURIComponent(contentId)}`)
}

export function createUserReview(contentId, payload) {
  return authorizedRequest(`/api/contents/${encodeURIComponent(contentId)}/reviews`, {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

export function getMyReviews() {
  return authorizedRequest('/api/my/reviews')
}

export function updateProfile(payload) {
  return authorizedRequest('/api/profile', {
    method: 'PATCH',
    body: JSON.stringify(payload),
  })
}
