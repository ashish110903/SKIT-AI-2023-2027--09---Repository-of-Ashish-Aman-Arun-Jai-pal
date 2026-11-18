/**
 * Cloudburst Early Warning & Alarm System - Emergency Alerts & Siren Synthesizer
 * Sprint 4: Display warning notification (create interface for showing emergency)
 * Author: Jai Pal (Frontend Lead)
 */

(function () {
  'use strict';

  // Audio Context & Siren State
  let audioCtx = null;
  let sirenOscillator = null;
  let sirenGain = null;
  let sirenInterval = null;
  let isSirenPlaying = false;
  let isAudioEnabled = true;

  // Active Alert Tracking
  let currentActiveAlert = null;

  /**
   * Initialize Web Audio API Synthesizer for Emergency Warning Siren
   */
  function initAudioContext() {
    if (!audioCtx) {
      const AudioContextClass = window.AudioContext || window.webkitAudioContext;
      if (AudioContextClass) {
        audioCtx = new AudioContextClass();
      }
    }
    if (audioCtx && audioCtx.state === 'suspended') {
      audioCtx.resume();
    }
  }

  /**
   * Start Emergency Alarm Siren (Pulsating two-tone emergency pitch)
   */
  function startSiren() {
    if (!isAudioEnabled) return;
    initAudioContext();
    if (!audioCtx || isSirenPlaying) return;

    try {
      sirenOscillator = audioCtx.createOscillator();
      sirenGain = audioCtx.createGain();

      sirenOscillator.type = 'sawtooth';
      sirenOscillator.frequency.setValueAtTime(650, audioCtx.currentTime);

      sirenGain.gain.setValueAtTime(0.15, audioCtx.currentTime); // controlled volume

      sirenOscillator.connect(sirenGain);
      sirenGain.connect(audioCtx.destination);

      sirenOscillator.start();
      isSirenPlaying = true;

      // Two-tone frequency modulation (650 Hz to 950 Hz sweep)
      let highTone = false;
      sirenInterval = setInterval(() => {
        if (!isSirenPlaying || !audioCtx) return;
        const targetFreq = highTone ? 650 : 950;
        sirenOscillator.frequency.exponentialRampToValueAtTime(targetFreq, audioCtx.currentTime + 0.35);
        highTone = !highTone;
      }, 400);

      updateAudioButtonUI(true);
    } catch (e) {
      console.warn('Audio synthesis not permitted without initial user interaction:', e);
    }
  }

  /**
   * Stop Emergency Alarm Siren
   */
  function stopSiren() {
    if (sirenInterval) {
      clearInterval(sirenInterval);
      sirenInterval = null;
    }
    if (sirenOscillator) {
      try {
        sirenOscillator.stop();
        sirenOscillator.disconnect();
      } catch (e) {}
      sirenOscillator = null;
    }
    isSirenPlaying = false;
    updateAudioButtonUI(false);
  }

  /**
   * Toggle Audio Siren Enabled/Muted state
   */
  function toggleAudio() {
    initAudioContext();
    isAudioEnabled = !isAudioEnabled;
    if (!isAudioEnabled && isSirenPlaying) {
      stopSiren();
    }
    updateAudioButtonUI(isSirenPlaying);
  }

  function updateAudioButtonUI(playing) {
    const icon = document.getElementById('audioIcon');
    const label = document.getElementById('audioLabel');
    if (!icon || !label) return;

    if (!isAudioEnabled) {
      icon.textContent = '🔇';
      label.textContent = 'Siren Muted';
    } else if (playing) {
      icon.textContent = '🔊';
      label.textContent = 'ALARM SOUNDING';
    } else {
      icon.textContent = '🔈';
      label.textContent = 'Siren Armed';
    }
  }

  /**
   * Display Emergency Warning Alert (Banner, Modal & Audio)
   */
  function triggerWarningAlert(alert) {
    currentActiveAlert = alert;

    // 1. Show Top Emergency Banner
    const banner = document.getElementById('emergencyBanner');
    const bannerStation = document.getElementById('bannerStation');
    if (banner) banner.classList.add('active');
    if (bannerStation) bannerStation.textContent = alert.stationId || 'Station-01';

    // 2. Open Emergency Modal
    const modal = document.getElementById('emergencyModal');
    const title = document.getElementById('modalAlertTitle');
    const desc = document.getElementById('modalAlertDesc');
    const time = document.getElementById('modalAlertTime');
    const stn = document.getElementById('modalAlertStation');

    if (modal) modal.classList.add('active');
    if (title) title.textContent = `CLOUDBURST ${alert.level} ACTIVATED`;
    if (desc) desc.textContent = alert.desc;
    if (time) time.textContent = new Date().toLocaleTimeString('en-IN') + ' IST';
    if (stn) stn.textContent = alert.stationId || 'Station-01';

    // 3. Sound Alarm
    startSiren();

    // 4. Append to Alert Dispatch Log
    logAlertEvent({
      time: new Date().toLocaleTimeString('en-IN'),
      station: alert.stationId || 'Station-01',
      level: alert.level,
      desc: alert.desc,
      status: 'Active Warning'
    });
  }

  /**
   * Dismiss Warning UI once condition clears
   */
  function dismissWarningAlert() {
    const banner = document.getElementById('emergencyBanner');
    if (banner) banner.classList.remove('active');
    stopSiren();
  }

  /**
   * Acknowledge Active Alert by Operator
   */
  function acknowledgeActiveAlert() {
    const modal = document.getElementById('emergencyModal');
    if (modal) modal.classList.remove('active');
    stopSiren();

    if (currentActiveAlert) {
      logAlertEvent({
        time: new Date().toLocaleTimeString('en-IN'),
        station: currentActiveAlert.stationId || 'Station-01',
        level: 'ACK',
        desc: 'Operator confirmed alert. Evacuation protocol & SMS broadcast dispatched.',
        status: 'Acknowledged'
      });
      currentActiveAlert = null;
    }
  }

  /**
   * Append an event to the Early Warning Notification Log table
   */
  function logAlertEvent(entry) {
    const tableBody = document.getElementById('alertsLogBody');
    if (!tableBody) return;

    const tr = document.createElement('tr');
    let badgeClass = 'trend-stable';
    if (entry.level === 'WARNING') badgeClass = 'trend-up';
    else if (entry.level === 'WATCH') badgeClass = 'trend-down';

    tr.innerHTML = `
      <td>${entry.time}</td>
      <td><strong>${entry.station}</strong></td>
      <td><span class="kpi-badge ${badgeClass}">${entry.level}</span></td>
      <td>${entry.desc}</td>
      <td>${entry.status}</td>
    `;

    // Keep log clean (last 10 events)
    if (tableBody.children.length > 10) {
      tableBody.removeChild(tableBody.lastElementChild);
    }
    tableBody.insertBefore(tr, tableBody.firstChild);
  }

  function clearAcks() {
    const tableBody = document.getElementById('alertsLogBody');
    if (tableBody) tableBody.innerHTML = '';
  }

  // Bind Buttons
  document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('btnAudioToggle')?.addEventListener('click', toggleAudio);
    document.getElementById('btnBannerMute')?.addEventListener('click', stopSiren);
  });

  window.AlertsManager = {
    triggerWarningAlert,
    dismissWarningAlert,
    acknowledgeActiveAlert,
    muteSiren: stopSiren,
    startSiren,
    toggleAudio,
    logAlertEvent,
    clearAcks
  };
})();
