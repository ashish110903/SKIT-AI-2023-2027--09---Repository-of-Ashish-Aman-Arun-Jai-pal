const BASE_URL = 'http://localhost:8000/api';
export async function fetchTelemetry() {
  const res = await fetch(`${BASE_URL}/telemetry/latest`);
  return res.json();
}
