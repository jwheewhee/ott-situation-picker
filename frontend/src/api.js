const API_BASE_URL = 'http://127.0.0.1:8000'

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

export function getSituationContents(situationName) {
  return request(`/api/situations/${encodeURIComponent(situationName)}/contents`)
}

export function getContentDetail(contentId) {
  return request(`/api/contents/${encodeURIComponent(contentId)}`)
}

export function createUserReview(contentId, payload) {
  return request(`/api/contents/${encodeURIComponent(contentId)}/reviews`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
}
