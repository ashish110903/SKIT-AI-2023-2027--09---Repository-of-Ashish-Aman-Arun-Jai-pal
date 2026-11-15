/**
 * Cloudburst Early Warning & Alarm System - AI/ML Risk Gauge Component
 * Sprint 3: Display the prediction result (show detected risk on dashboard)
 * Author: Jai Pal (Frontend Lead)
 */

(function () {
  'use strict';

  // SVG Gauge Arc Circumference: 283 px (half-circle r=90)
  const MAX_STROKE_OFFSET = 283;

  /**
   * Update the Risk Assessment Display based on ML Output
   * @param {number} probability - Cloudburst probability percentage (0 to 100)
   * @param {Object} factors - Precursor atmospheric anomaly indicators
   */
  function updateRisk(probability, factors) {
    const clampedProb = Math.max(0, Math.min(100, probability));

    // Calculate stroke offset
    // 0% -> 283 (empty), 100% -> 0 (full arc)
    const offset = MAX_STROKE_OFFSET - (clampedProb / 100) * MAX_STROKE_OFFSET;

    const arc = document.getElementById('gaugeArc');
    const probText = document.getElementById('riskPercentage');
    const badge = document.getElementById('riskLevelBadge');

    if (arc) {
      arc.style.strokeDashoffset = offset;
    }

    if (probText) {
      probText.textContent = `${clampedProb.toFixed(1)}%`;
    }

    // Determine Risk Level Tier
    let level = 'NORMAL';
    let badgeClass = 'risk-badge normal';
    let strokeColor = 'var(--status-normal)';

    if (clampedProb >= 75) {
      level = 'LEVEL 2: CLOUDBURST WARNING';
      badgeClass = 'risk-badge warning';
      strokeColor = 'var(--status-warning)';
    } else if (clampedProb >= 35) {
      level = 'LEVEL 1: ELEVATED WATCH';
      badgeClass = 'risk-badge watch';
      strokeColor = 'var(--status-watch)';
    } else {
      level = 'LEVEL 0: NORMAL';
      badgeClass = 'risk-badge normal';
      strokeColor = 'var(--status-normal)';
    }

    if (arc) arc.style.stroke = strokeColor;
    if (badge) {
      badge.className = badgeClass;
      badge.textContent = level;
    }

    // Update Anomaly Checklist Factors
    if (factors) {
      const fPressure = document.getElementById('factorPressure');
      const fRain = document.getElementById('factorRain');
      const fMoisture = document.getElementById('factorMoisture');

      if (fPressure) {
        fPressure.textContent = factors.pressureDrop || 'Normal (-0.2 hPa)';
        fPressure.style.color = clampedProb > 70 ? 'var(--color-rose)' : 'var(--text-main)';
      }
      if (fRain) {
        fRain.textContent = factors.rainSpike || 'Sub-threshold (<10 mm/h)';
        fRain.style.color = clampedProb > 70 ? 'var(--color-rose)' : 'var(--text-main)';
      }
      if (fMoisture) {
        fMoisture.textContent = factors.moisture || 'Nominal';
        fMoisture.style.color = clampedProb > 50 ? 'var(--color-amber)' : 'var(--text-main)';
      }
    }

    // Notify Alert Manager if Warning Threshold is crossed
    if (clampedProb >= 75 && window.AlertsManager) {
      window.AlertsManager.triggerWarningAlert({
        level: 'WARNING',
        probability: clampedProb,
        stationId: window.App?.getState()?.activeStationId || 'STN-01',
        desc: `High probability (${clampedProb.toFixed(1)}%) of cloudburst detected. Rapid pressure plunge and intense localized convective cell identified.`
      });
    } else if (clampedProb < 75 && window.AlertsManager) {
      window.AlertsManager.dismissWarningAlert();
    }
  }

  window.RiskGauge = {
    updateRisk
  };

  document.addEventListener('DOMContentLoaded', () => {
    // Initial display
    updateRisk(4.2, {
      pressureDrop: 'Normal (-0.15 hPa/15m)',
      rainSpike: 'Sub-threshold (<5 mm/h)',
      moisture: 'Nominal (72% RH)'
    });
  });
})();
