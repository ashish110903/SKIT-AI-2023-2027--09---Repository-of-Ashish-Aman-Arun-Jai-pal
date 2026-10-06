/**
 * Cloudburst Early Warning & Alarm System - Main Application Controller
 * Author: Jai Pal (Frontend Lead)
 * Project ID: SKIT/AI/2023-2027/09
 */

(function () {
  'use strict';

  // Mountain Sensor Stations Configuration
  const STATIONS = [
    {
      id: 'STN-01',
      name: 'Station-01 (Mussoorie Ridge)',
      altitude: '2,005 m ASL',
      coords: '30.4598° N, 78.0644° E',
      status: 'normal',
      battery: '94%',
      signal: '-74 dBm (Excellent)'
    },
    {
      id: 'STN-02',
      name: 'Station-02 (Kedarnath Valley)',
      altitude: '3,583 m ASL',
      coords: '30.7346° N, 79.0669° E',
      status: 'normal',
      battery: '88%',
      signal: '-82 dBm (Good)'
    },
    {
      id: 'STN-03',
      name: 'Station-03 (Shimla Peak)',
      altitude: '2,276 m ASL',
      coords: '31.1048° N, 77.1734° E',
      status: 'normal',
      battery: '91%',
      signal: '-79 dBm (Good)'
    },
    {
      id: 'STN-04',
      name: 'Station-04 (Nainital Slopes)',
      altitude: '2,084 m ASL',
      coords: '29.3919° N, 79.4542° E',
      status: 'normal',
      battery: '85%',
      signal: '-86 dBm (Moderate)'
    }
  ];

  // Application State
  const AppState = {
    activeStationId: 'STN-01',
    isOnline: true,
    lastSyncTime: new Date(),
    currentReadings: {
      rainfallRate: 0.0,
      rainAccum1h: 0.0,
      pressure: 1013.25,
      pressureDropRate: -0.15,
      temperature: 21.5,
      dewPoint: 18.2,
      humidity: 72,
      cloudburstRisk: 4.2,
      riskLevel: 'NORMAL'
    }
  };

  /**
   * Initialize Station Navigation Tabs
   */
  function initStationTabs() {
    const container = document.getElementById('stationTabsContainer');
    if (!container) return;
    container.innerHTML = '';

    STATIONS.forEach((station) => {
      const tab = document.createElement('button');
      tab.className = `station-tab ${station.id === AppState.activeStationId ? 'active' : ''} ${station.status === 'warning' ? 'danger' : ''}`;
      tab.id = `tab-${station.id}`;
      tab.innerHTML = `
        <span class="tab-status-dot"></span>
        <span>${station.name.split(' (')[0]}</span>
      `;
      tab.onclick = () => switchStation(station.id);
      container.appendChild(tab);
    });
  }

  /**
   * Switch the active monitored station
   */
  function switchStation(stationId) {
    AppState.activeStationId = stationId;
    const station = STATIONS.find(s => s.id === stationId);
    if (!station) return;

    // Update active tab styling
    document.querySelectorAll('.station-tab').forEach(t => t.classList.remove('active'));
    const activeTab = document.getElementById(`tab-${stationId}`);
    if (activeTab) activeTab.classList.add('active');

    // Update metadata card
    const metaName = document.getElementById('metaStationName');
    const metaAlt = document.getElementById('metaAltitude');
    const metaCoords = document.getElementById('metaCoords');
    const metaSignal = document.getElementById('metaSignal');
    const metaBattery = document.getElementById('nodeBattery');
    const chartStation = document.getElementById('chartStationName');

    if (metaName) metaName.textContent = station.name;
    if (metaAlt) metaAlt.textContent = station.altitude;
    if (metaCoords) metaCoords.textContent = station.coords;
    if (metaSignal) metaSignal.textContent = station.signal;
    if (metaBattery) metaBattery.textContent = `🔋 Battery: ${station.battery}`;
    if (chartStation) chartStation.textContent = station.name.split(' (')[0];

    // Trigger chart reset / reload for selected station
    if (window.TelemetryCharts) {
      window.TelemetryCharts.loadStationData(stationId);
    }
  }

  /**
   * Update the live digital clock and date
   */
  function updateClock() {
    const now = new Date();
    const timeStr = now.toLocaleTimeString('en-IN', { hour12: false }) + ' IST';
    const dateStr = now.toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric' });

    const clockTime = document.getElementById('liveClock');
    const clockDate = document.getElementById('liveDate');
    if (clockTime) clockTime.textContent = timeStr;
    if (clockDate) clockDate.textContent = dateStr;
  }

  /**
   * Update KPI card displays with fresh telemetry readings
   */
  function updateKpiCards(data) {
    if (!data) return;

    // Rainfall
    const valRain = document.getElementById('valRainfall');
    const valAccum = document.getElementById('valRainAccum');
    const badgeRain = document.getElementById('badgeRainTrend');
    if (valRain) valRain.textContent = Number(data.rainfallRate).toFixed(1);
    if (valAccum) valAccum.textContent = `${Number(data.rainAccum1h || data.rainfallRate * 0.8).toFixed(1)} mm`;
    if (badgeRain) {
      if (data.rainfallRate > 50) {
        badgeRain.className = 'kpi-badge trend-up';
        badgeRain.textContent = 'TORRENTIAL';
      } else if (data.rainfallRate > 15) {
        badgeRain.className = 'kpi-badge trend-up';
        badgeRain.textContent = 'HEAVY';
      } else {
        badgeRain.className = 'kpi-badge trend-stable';
        badgeRain.textContent = 'STABLE';
      }
    }

    // Pressure
    const valPressure = document.getElementById('valPressure');
    const valDrop = document.getElementById('valPressureDrop');
    const badgePressure = document.getElementById('badgePressureTrend');
    if (valPressure) valPressure.textContent = Number(data.pressure).toFixed(1);
    if (valDrop) valDrop.textContent = `${Number(data.pressureDropRate).toFixed(1)} hPa/h`;
    if (badgePressure) {
      if (data.pressureDropRate < -3.0) {
        badgePressure.className = 'kpi-badge trend-up';
        badgePressure.textContent = 'RAPID PLUNGE';
      } else if (data.pressureDropRate < -1.5) {
        badgePressure.className = 'kpi-badge trend-down';
        badgePressure.textContent = 'FALLING';
      } else {
        badgePressure.className = 'kpi-badge trend-stable';
        badgePressure.textContent = 'NORMAL';
      }
    }

    // Temperature
    const valTemp = document.getElementById('valTemp');
    const valDew = document.getElementById('valDewPoint');
    if (valTemp) valTemp.textContent = Number(data.temperature).toFixed(1);
    if (valDew) valDew.textContent = `${Number(data.dewPoint || (data.temperature - 3.2)).toFixed(1)} °C`;

    // Humidity
    const valHum = document.getElementById('valHumidity');
    const valVapor = document.getElementById('valVaporSat');
    if (valHum) valHum.textContent = Math.round(data.humidity);
    if (valVapor) {
      if (data.humidity > 95) valVapor.textContent = 'Saturated (High Risk)';
      else if (data.humidity > 80) valVapor.textContent = 'High';
      else valVapor.textContent = 'Moderate';
    }

    // Update AppState
    Object.assign(AppState.currentReadings, data);
  }

  // Application Bootstrapping
  function init() {
    initStationTabs();
    updateClock();
    setInterval(updateClock, 1000);

    // Initial KPI population
    updateKpiCards(AppState.currentReadings);

    console.log('[Jai Pal - Frontend] Cloudburst Monitoring Dashboard initialized successfully.');
  }

  window.App = {
    getState: () => AppState,
    getStations: () => STATIONS,
    updateKpiCards,
    switchStation
  };

  document.addEventListener('DOMContentLoaded', init);
})();
