#ifndef POWER_MGMT_H
#define POWER_MGMT_H
#include <esp_sleep.h>

#define TIME_TO_SLEEP_SEC 600

void enterDeepSleep() {
  esp_sleep_enable_timer_wakeup(TIME_TO_SLEEP_SEC * 1000000ULL);
  esp_deep_sleep_start();
}
#endif
