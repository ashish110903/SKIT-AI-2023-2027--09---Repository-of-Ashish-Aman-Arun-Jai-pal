export function renderGauge(val) {
  const deg = (val / 100) * 180;
  return `<div class='gauge'><div class='needle' style='transform: rotate(${deg}deg)'></div></div>`;
}
