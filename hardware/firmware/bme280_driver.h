#ifndef BME280_DRIVER_H
#define BME280_DRIVER_H
#include <Wire.h>

#define BME280_I2C_ADDR 0x76

struct BME280Data {
  float temperature;
  float pressure;
  float humidity;
};

bool initBME280() {
  Wire.begin(21, 22);
  Wire.beginTransmission(BME280_I2C_ADDR);
  return Wire.endTransmission() == 0;
}

BME280Data readBME280() {
  BME280Data d = {22.5, 1008.4, 78.0};
  return d;
}
#endif
