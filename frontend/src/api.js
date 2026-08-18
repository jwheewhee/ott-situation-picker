const API_BASE_URL = 'http://127.0.0.1:8000'

async function fetchJson(path) {
  const response = await fetch(`${API_BASE_URL}${path}`)
  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`)
  }
  return response.json()
}

export function getSituationContents(situationName) {
  return fetchJson(`/api/situations/${encodeURIComponent(situationName)}/contents`)
}

export function getContentDetail(contentId) {
  return fetchJson(`/api/contents/${encodeURIComponent(contentId)}`)
}
