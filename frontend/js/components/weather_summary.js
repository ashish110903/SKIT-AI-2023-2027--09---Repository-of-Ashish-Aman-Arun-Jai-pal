export function renderWeatherSummary(data) {
  return `<div class='summary-card'><h4>Atmospheric Status</h4><p>Dew point: ${data.dewPoint || 'Normal'}</p></div>`;
}
