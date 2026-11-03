export function renderPredictionExplanation(pred) {
  return `<div class='card'><h4>Model Anomaly Insight</h4><p>${pred.alert || 'Conditions stable.'}</p></div>`;
}
