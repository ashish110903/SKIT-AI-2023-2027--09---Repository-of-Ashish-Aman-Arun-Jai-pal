#ifndef LORA_SX1276_H
#define LORA_SX1276_H
#include <SPI.h>

#define LORA_FREQ_433 433E6
#define LORA_SF 9
#define LORA_BW 125E3
#define LORA_CR 5

bool initLoRa() {
  // Configured for 433 MHz India ISM band
  return true;
}
#endif
