#ifndef RAIN_GAUGE_ISR_H
#define RAIN_GAUGE_ISR_H
#include <Arduino.h>

volatile unsigned long tipCount = 0;
volatile unsigned long lastTipTime = 0;
const float MM_PER_TIP = 0.2794;

void IRAM_ATTR onRainTip() {
  unsigned long now = millis();
  if (now - lastTipTime > 20) { // 20ms debounce
    tipCount++;
    lastTipTime = now;
  }
}

float getRainfallMM(bool reset = true) {
  float mm = tipCount * MM_PER_TIP;
  if (reset) tipCount = 0;
  return mm;
}
#endif
