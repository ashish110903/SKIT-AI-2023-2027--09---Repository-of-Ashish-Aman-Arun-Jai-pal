/**
 * Cloudburst Early Warning & Alarm System - Sensor Telemetry Visualizer
 * Sprint 2: Display sensor data on dashboard (Rainfall, Pressure, Temp, Humidity)
 * Author: Jai Pal (Frontend Lead)
 */

(function () {
  'use strict';

  let telemetryChart = null;
  let currentMode = 'combined'; // 'combined' | 'rainfall' | 'pressure'

  // Rolling buffer configuration (last 12 readings)
  const MAX_DATA_POINTS = 12;

  // Initial synthetic mountain telemetry history
  const chartData = {
    labels: ['-55m', '-50m', '-45m', '-40m', '-35m', '-30m', '-25m', '-20m', '-15m', '-10m', '-5m', 'Now'],
    rainfall: [0.0, 0.0, 0.2, 0.4, 0.8, 1.2, 2.5, 3.8, 4.2, 4.0, 3.5, 0.0],
    pressure: [1014.2, 1014.0, 1013.9, 1013.8, 1013.6, 1013.5, 1013.4, 1013.2, 1013.1, 1013.0, 1013.1, 1013.2],
    temperature: [22.4, 22.2, 22.0, 21.9, 21.8, 21.7, 21.6, 21.5, 21.4, 21.4, 21.5, 21.5],
    humidity: [68, 69, 70, 71, 71, 72, 73, 73, 74, 74, 73, 72]
  };

  /**
   * Initialize Chart.js Instance
   */
  function initChart() {
    const canvas = document.getElementById('telemetryChart');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');

    // Chart datasets configuration
    const datasets = [
      {
        label: 'Rainfall Rate (mm/h)',
        data: [...chartData.rainfall],
        borderColor: '#06b6d4',
        backgroundColor: 'rgba(6, 182, 212, 0.15)',
        borderWidth: 2.5,
        fill: true,
        tension: 0.35,
        yAxisID: 'yRain',
        pointRadius: 3,
        pointHoverRadius: 6
      },
      {
        label: 'Atmospheric Pressure (hPa)',
        data: [...chartData.pressure],
        borderColor: '#f59e0b',
        backgroundColor: 'transparent',
        borderWidth: 2,
        borderDash: [4, 4],
        tension: 0.25,
        yAxisID: 'yPressure',
        pointRadius: 3,
        pointHoverRadius: 6
      },
      {
        label: 'Relative Humidity (%)',
        data: [...chartData.humidity],
        borderColor: '#6366f1',
        backgroundColor: 'transparent',
        borderWidth: 1.5,
        tension: 0.3,
        yAxisID: 'yHumidity',
        pointRadius: 2,
        pointHoverRadius: 5
      }
    ];

    telemetryChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: chartData.labels,
        datasets: datasets
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        animation: {
          duration: 450
        },
        interaction: {
          mode: 'index',
          intersect: false
        },
        plugins: {
          legend: {
            position: 'top',
            labels: {
              color: '#9ca3af',
              font: { size: 11, family: 'inherit' },
              boxWidth: 12
            }
          },
          tooltip: {
            backgroundColor: '#1f2937',
            titleColor: '#f9fafb',
            bodyColor: '#e5e7eb',
            borderColor: '#374151',
            borderWidth: 1,
            padding: 10
          }
        },
        scales: {
          x: {
            grid: { color: 'rgba(55, 65, 81, 0.3)' },
            ticks: { color: '#9ca3af', font: { size: 10 } }
          },
          yRain: {
            type: 'linear',
            position: 'left',
            title: { display: true, text: 'Rainfall (mm/h)', color: '#06b6d4', font: { size: 10 } },
            min: 0,
            max: 100,
            grid: { color: 'rgba(55, 65, 81, 0.2)' },
            ticks: { color: '#06b6d4', font: { size: 10 } }
          },
          yPressure: {
            type: 'linear',
            position: 'right',
            title: { display: true, text: 'Pressure (hPa)', color: '#f59e0b', font: { size: 10 } },
            min: 990,
            max: 1030,
            grid: { drawOnChartArea: false },
            ticks: { color: '#f59e0b', font: { size: 10 } }
          },
          yHumidity: {
            type: 'linear',
            position: 'right',
            display: false,
            min: 0,
            max: 100
          }
        }
      }
    });
  }

  /**
   * Append a new real-time reading to the chart stream
   */
  function appendDataPoint(label, rain, pressure, temp, humidity) {
    if (!telemetryChart) return;

    chartData.labels.shift();
    chartData.labels.push(label || 'Now');

    chartData.rainfall.shift();
    chartData.rainfall.push(rain);

    chartData.pressure.shift();
    chartData.pressure.push(pressure);

    chartData.temperature.shift();
    chartData.temperature.push(temp);

    chartData.humidity.shift();
    chartData.humidity.push(humidity);

    telemetryChart.data.labels = [...chartData.labels];
    telemetryChart.data.datasets[0].data = [...chartData.rainfall];
    telemetryChart.data.datasets[1].data = [...chartData.pressure];
    telemetryChart.data.datasets[2].data = [...chartData.humidity];

    telemetryChart.update('none'); // high-performance update without complete re-animation
  }

  /**
   * Switch chart filter view (All vs Rainfall vs Pressure)
   */
  function switchView(mode) {
    if (!telemetryChart) return;
    currentMode = mode;

    document.querySelectorAll('.btn-chart-toggle').forEach(btn => btn.classList.remove('active'));

    if (mode === 'combined') {
      document.getElementById('btnToggleCombined')?.classList.add('active');
      telemetryChart.data.datasets[0].hidden = false;
      telemetryChart.data.datasets[1].hidden = false;
      telemetryChart.data.datasets[2].hidden = false;
    } else if (mode === 'rainfall') {
      document.getElementById('btnToggleRain')?.classList.add('active');
      telemetryChart.data.datasets[0].hidden = false;
      telemetryChart.data.datasets[1].hidden = true;
      telemetryChart.data.datasets[2].hidden = true;
    } else if (mode === 'pressure') {
      document.getElementById('btnTogglePressure')?.classList.add('active');
      telemetryChart.data.datasets[0].hidden = true;
      telemetryChart.data.datasets[1].hidden = false;
      telemetryChart.data.datasets[2].hidden = true;
    }

    telemetryChart.update();
  }

  /**
   * Reset data buffers when switching stations
   */
  function loadStationData(stationId) {
    // Generate slight baseline variation per station altitude
    const basePressure = stationId === 'STN-02' ? 965.0 : 1012.0;
    for (let i = 0; i < MAX_DATA_POINTS; i++) {
      chartData.rainfall[i] = (Math.random() * 2.0).toFixed(1);
      chartData.pressure[i] = (basePressure + (Math.random() * 0.8 - 0.4)).toFixed(1);
      chartData.humidity[i] = Math.round(65 + Math.random() * 10);
    }
    if (telemetryChart) {
      telemetryChart.options.scales.yPressure.min = Math.floor(basePressure - 20);
      telemetryChart.options.scales.yPressure.max = Math.ceil(basePressure + 20);
      telemetryChart.update();
    }
  }

  window.TelemetryCharts = {
    initChart,
    appendDataPoint,
    switchView,
    loadStationData,
    getData: () => chartData
  };

  document.addEventListener('DOMContentLoaded', () => {
    // Slight delay to ensure canvas context is measured properly
    setTimeout(initChart, 50);
  });
})();
