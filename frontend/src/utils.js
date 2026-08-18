const SENTIMENT_CLASS_BY_LABEL = {
  긍정: 'positive',
  중립: 'neutral',
  부정: 'negative',
}

export function sentimentClass(label) {
  return SENTIMENT_CLASS_BY_LABEL[label] ?? 'neutral'
}
