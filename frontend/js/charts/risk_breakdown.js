export function renderRiskBreakdown(ctx, data) {
  return new Chart(ctx, { type: 'bar', data: { labels: ['Rainfall Rate', 'Pressure Drop', 'Humidity Saturation'], datasets: [{ data: [data.rainScore, data.pressureScore, data.humidityScore] }] } });
}
