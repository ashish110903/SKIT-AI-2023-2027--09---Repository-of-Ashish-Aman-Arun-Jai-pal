export function createStatusPill(isOnline) {
  return `<span class='pill ${isOnline ? 'pill-online' : 'pill-offline'}'>${isOnline ? 'ONLINE' : 'OFFLINE'}</span>`;
}
