export function triggerEmergencyBanner(msg) {
  const b = document.getElementById('emergency-banner');
  if (b) { b.innerText = `🚨 CRITICAL ALARM: ${msg}`; b.style.display = 'block'; }
}
