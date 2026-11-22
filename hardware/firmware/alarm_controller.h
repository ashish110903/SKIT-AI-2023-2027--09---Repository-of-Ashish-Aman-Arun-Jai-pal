#ifndef ALARM_CONTROLLER_H
#define ALARM_CONTROLLER_H
#include <Arduino.h>

void soundCriticalAlarm(uint8_t buzzerPin, uint8_t ledPin) {
  for (int i = 0; i < 5; i++) {
    digitalWrite(ledPin, HIGH);
    tone(buzzerPin, 2400, 150);
    delay(200);
    digitalWrite(ledPin, LOW);
    delay(100);
  }
}
#endif
