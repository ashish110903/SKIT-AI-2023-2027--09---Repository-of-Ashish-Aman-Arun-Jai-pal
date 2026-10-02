export function initRainfallChart(ctx) {
  return new Chart(ctx, { type: 'line', data: { labels: [], datasets: [{ label: 'Rainfall (mm/hr)', data: [], borderColor: '#38bdf8' }] } });
}
