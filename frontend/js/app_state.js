export const AppState = {
  stationId: 'ST-01',
  currentReading: null,
  riskLevel: 'LOW',
  alerts: [],
  listeners: [],
  subscribe(fn) { this.listeners.push(fn); }
};
