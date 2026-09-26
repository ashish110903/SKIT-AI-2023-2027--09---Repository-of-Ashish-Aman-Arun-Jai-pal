#include <Arduino.h>

#define RAIN_PIN 34
#define BUZZER_PIN 26
#define LED_PIN 25

void setup() {
  Serial.begin(115200);
  pinMode(RAIN_PIN, INPUT_PULLUP);
  pinMode(BUZZER_PIN, OUTPUT);
  pinMode(LED_PIN, OUTPUT);
  Serial.println(F("Cloudburst ESP32 Node Initialized"));
}

void loop() {
  delay(1000);
}
