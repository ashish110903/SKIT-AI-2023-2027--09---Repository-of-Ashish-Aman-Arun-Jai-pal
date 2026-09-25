export function createMetricCard(title, value, unit, icon) {
  return `<div class='card metric-card'><h3>${title}</h3><div class='val'>${value} <small>${unit}</small></div></div>`;
}
