/**
 * Cloudburst Early Warning & Alarm System - Backend Integration Service
 * Sprint 5: Connect dashboard with backend (fetch and display real-time data from backend)
 * Author: Jai Pal (Frontend Lead)
 */

(function () {
  'use strict';

  // FastAPI Backend Configuration
  const API_CONFIG = {
    baseUrl: 'http://localhost:8000/api/v1',
    pollIntervalMs: 5000,
    retryDelayMs: 3000,
    timeoutMs: 4000
  };

  let pollTimer = null;
  let isBackendConnected = false;

  /**
   * Safe fetch with timeout
   */
  async function fetchWithTimeout(resource, options = {}) {
    const { timeout = API_CONFIG.timeoutMs } = options;
    const controller = new AbortController();
    const id = setTimeout(() => controller.abort(), timeout);

    try {
      const response = await fetch(resource, {
        ...options,
        signal: controller.signal
      });
      clearTimeout(id);
      return response;
    } catch (err) {
      clearTimeout(id);
      throw err;
    }
  }

  /**
   * Fetch latest telemetry readings from FastAPI backend
   */
  async function fetchLatestTelemetry(stationId) {
    try {
      const url = `${API_CONFIG.baseUrl}/sensors/latest?station_id=${stationId || 'STN-01'}`;
      const res = await fetchWithTimeout(url);

      if (!res.ok) throw new Error(`HTTP error ${res.status}`);
      const data = await res.json();

      setConnectionStatus(true, 'Backend Connected (FastAPI)');
      return data;
    } catch (err) {
      setConnectionStatus(false, 'Operating Offline (LoRa Cache)');
      return null;
    }
  }

  /**
   * Fetch active alerts from backend
   */
  async function fetchActiveAlerts() {
    try {
      const url = `${API_CONFIG.baseUrl}/alerts/active`;
      const res = await fetchWithTimeout(url);
      if (!res.ok) throw new Error(`HTTP error ${res.status}`);
      return await res.json();
    } catch (err) {
      return null;
    }
  }

  /**
   * Fetch real-time AI/ML prediction score from backend
   */
  async function fetchPredictionStatus(stationId) {
    try {
      const url = `${API_CONFIG.baseUrl}/predict/status?station_id=${stationId || 'STN-01'}`;
      const res = await fetchWithTimeout(url);
      if (!res.ok) throw new Error(`HTTP error ${res.status}`);
      return await res.json();
    } catch (err) {
      return null;
    }
  }

  /**
   * Update Network Badge UI
   */
  function setConnectionStatus(connected, message) {
    isBackendConnected = connected;
    const badge = document.getElementById('networkBadge');
    const text = document.getElementById('networkText');

    if (badge && text) {
      if (connected) {
        badge.className = 'network-badge';
        text.textContent = message || 'FastAPI Backend: Live';
      } else {
        badge.className = 'network-badge offline';
        text.textContent = message || 'Offline / Poor Connectivity';
      }
    }
  }

  /**
   * Continuous Polling Loop for live sensor updates
   */
  async function syncCycle() {
    const activeStation = window.App?.getState()?.activeStationId || 'STN-01';

    // 1. Fetch sensor telemetry
    const telemetry = await fetchLatestTelemetry(activeStation);
    if (telemetry) {
      // Update UI components
      window.App.updateKpiCards(telemetry);

      if (window.TelemetryCharts) {
        const nowLabel = new Date().toLocaleTimeString('en-IN', { minute: '2-digit', second: '2-digit' });
        window.TelemetryCharts.appendDataPoint(
          nowLabel,
          telemetry.rainfallRate,
          telemetry.pressure,
          telemetry.temperature,
          telemetry.humidity
        );
      }
    }

    // 2. Fetch ML prediction score
    const prediction = await fetchPredictionStatus(activeStation);
    if (prediction && window.RiskGauge) {
      window.RiskGauge.updateRisk(prediction.probability, prediction.factors);
    }

    // 3. Check active alerts
    const alerts = await fetchActiveAlerts();
    if (alerts && alerts.length > 0 && window.AlertsManager) {
      const highest = alerts[0];
      if (highest.level === 'WARNING') {
        window.AlertsManager.triggerWarningAlert(highest);
      }
    }
  }

  /**
   * Start background polling synchronization
   */
  function startSync() {
    if (pollTimer) clearInterval(pollTimer);
    syncCycle(); // immediate first try
    pollTimer = setInterval(syncCycle, API_CONFIG.pollIntervalMs);
  }

  function stopSync() {
    if (pollTimer) {
      clearInterval(pollTimer);
      pollTimer = null;
    }
  }

  window.BackendAPI = {
    fetchLatestTelemetry,
    fetchActiveAlerts,
    fetchPredictionStatus,
    startSync,
    stopSync,
    setConnectionStatus,
    isConnected: () => isBackendConnected
  };

  document.addEventListener('DOMContentLoaded', () => {
    // Start background sync
    startSync();
  });
})();
