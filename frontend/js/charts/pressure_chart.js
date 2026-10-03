export function initPressureChart(ctx) {
  return new Chart(ctx, { type: 'line', data: { labels: [], datasets: [{ label: 'Pressure (hPa)', data: [], borderColor: '#f43f5e' }] } });
}
