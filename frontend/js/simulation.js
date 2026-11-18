/**
 * Cloudburst Early Warning & Alarm System - Simulation Control & Test Harness
 * Sprint 6: Test the complete dashboard (test dashboard with real project data & alerts)
 * Author: Jai Pal (Frontend Lead)
 */

(function () {
  'use strict';

  /**
   * Scenario 1: Normal Mountain Weather
   */
  function triggerNormal() {
    const data = {
      rainfallRate: (Math.random() * 0.8).toFixed(1),
      rainAccum1h: 0.2,
      pressure: (1013.2 + (Math.random() * 0.4 - 0.2)).toFixed(1),
      pressureDropRate: -0.15,
      temperature: 21.5,
      dewPoint: 17.8,
      humidity: 68
    };

    window.App.updateKpiCards(data);

    if (window.TelemetryCharts) {
      const now = new Date().toLocaleTimeString('en-IN', { minute: '2-digit', second: '2-digit' });
      window.TelemetryCharts.appendDataPoint(now, data.rainfallRate, data.pressure, data.temperature, data.humidity);
    }

    if (window.RiskGauge) {
      window.RiskGauge.updateRisk(3.8, {
        pressureDrop: 'Normal (-0.15 hPa/15m)',
        rainSpike: 'Nominal (<1.0 mm/h)',
        moisture: 'Moderate (68% RH)'
      });
    }

    if (window.AlertsManager) {
      window.AlertsManager.dismissWarningAlert();
      window.AlertsManager.logAlertEvent({
        time: new Date().toLocaleTimeString('en-IN'),
        station: window.App.getState().activeStationId,
        level: 'INFO',
        desc: 'Atmospheric conditions returned to normal stable mountain baseline.',
        status: 'Resolved'
      });
    }
  }

  /**
   * Scenario 2: Elevated Convective Activity (Watch Status)
   */
  function triggerWatch() {
    const data = {
      rainfallRate: 22.4,
      rainAccum1h: 14.8,
      pressure: 1008.6,
      pressureDropRate: -1.9,
      temperature: 18.8,
      dewPoint: 17.5,
      humidity: 86
    };

    window.App.updateKpiCards(data);

    if (window.TelemetryCharts) {
      const now = new Date().toLocaleTimeString('en-IN', { minute: '2-digit', second: '2-digit' });
      window.TelemetryCharts.appendDataPoint(now, data.rainfallRate, data.pressure, data.temperature, data.humidity);
    }

    if (window.RiskGauge) {
      window.RiskGauge.updateRisk(52.6, {
        pressureDrop: 'Elevated (-1.9 hPa/15m)',
        rainSpike: 'Moderate to Heavy (22.4 mm/h)',
        moisture: 'High (86% RH)'
      });
    }

    if (window.AlertsManager) {
      window.AlertsManager.logAlertEvent({
        time: new Date().toLocaleTimeString('en-IN'),
        station: window.App.getState().activeStationId,
        level: 'WATCH',
        desc: 'Convective cloud cluster detected. Moderate rainfall increase.',
        status: 'Advisory Active'
      });
    }
  }

  /**
   * Scenario 3: Extreme Cloudburst Emergency (Warning Status)
   */
  function triggerCloudburst() {
    const activeStation = window.App?.getState()?.activeStationId || 'STN-01';

    const data = {
      rainfallRate: 88.5,
      rainAccum1h: 56.2,
      pressure: 996.4,
      pressureDropRate: -5.8,
      temperature: 15.4,
      dewPoint: 15.2,
      humidity: 98
    };

    window.App.updateKpiCards(data);

    if (window.TelemetryCharts) {
      const now = new Date().toLocaleTimeString('en-IN', { minute: '2-digit', second: '2-digit' });
      window.TelemetryCharts.appendDataPoint(now, data.rainfallRate, data.pressure, data.temperature, data.humidity);
    }

    if (window.RiskGauge) {
      window.RiskGauge.updateRisk(96.4, {
        pressureDrop: 'CRITICAL PLUNGE (-5.8 hPa/15m)',
        rainSpike: 'TORRENTIAL (88.5 mm/h)',
        moisture: 'Saturated (98% RH)'
      });
    }

    if (window.AlertsManager) {
      window.AlertsManager.triggerWarningAlert({
        level: 'WARNING',
        probability: 96.4,
        stationId: activeStation,
        desc: `IMMEDIATE EVACUATION: Extreme cloudburst rate (88.5 mm/h) & barometric plunge at ${activeStation}. High danger of flash flood & debris flow.`
      });
    }
  }

  /**
   * Run automated tests and display results in modal
   */
  function runAutomatedTests() {
    if (window.DashboardTester) {
      window.DashboardTester.runAll();
    } else {
      alert('Test suite module is initializing, please retry.');
    }
  }

  window.SimulationEngine = {
    triggerNormal,
    triggerWatch,
    triggerCloudburst,
    runAutomatedTests
  };
})();
