import { fetchTelemetry } from './api.js';
import { setText } from './utils/dom_helpers.js';

export async function updateUI() {
  const d = await fetchTelemetry();
  setText('#rain-val', d.rainfall_mm);
}
