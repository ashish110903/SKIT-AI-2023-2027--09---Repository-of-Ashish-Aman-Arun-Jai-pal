export function renderRiskMeter(level) {
  const colors = { LOW: '#22c55e', MODERATE: '#eab308', HIGH: '#f97316', CRITICAL: '#dc2626' };
  return `<div class='risk-badge' style='background:${colors[level]}'>RISK: ${level}</div>`;
}
