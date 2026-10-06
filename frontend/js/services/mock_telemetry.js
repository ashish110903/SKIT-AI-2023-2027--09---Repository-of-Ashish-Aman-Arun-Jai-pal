export function startMockTelemetry(callback) {
  setInterval(() => {
    callback({
      rainfall: (Math.random() * 35).toFixed(1),
      pressure: (1005 - Math.random() * 8).toFixed(1),
      humidity: (80 + Math.random() * 15).toFixed(0)
    });
  }, 3000);
}
