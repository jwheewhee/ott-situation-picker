const SENTIMENT_CLASS_BY_LABEL = {
  긍정: 'positive',
  중립: 'neutral',
  부정: 'negative',
}

export function sentimentClass(label) {
  return SENTIMENT_CLASS_BY_LABEL[label] ?? 'neutral'
}

export function renderStars(rating) {
  const fullStars = Math.max(0, Math.min(5, Math.round(rating ?? 0)))
  return '★'.repeat(fullStars) + '☆'.repeat(5 - fullStars)
}
