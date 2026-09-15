# Pinout & Power Budget

| Signal | ESP32 GPIO | Mode |
|---|---|---|
| Rain Interrupt | GPIO 34 | INPUT_PULLUP (ISR) |
| BME280 SDA | GPIO 21 | I2C Data |
| BME280 SCL | GPIO 22 | I2C Clock |
| LoRa NSS | GPIO 5 | SPI CS |
| LoRa SCK | GPIO 18 | SPI Clock |
| LoRa MISO | GPIO 19 | SPI MISO |
| LoRa MOSI | GPIO 23 | SPI MOSI |
| Buzzer Alarm | GPIO 26 | OUTPUT PWM |
| Red Warning LED | GPIO 25 | OUTPUT |

Battery: 3.7V 3200mAh 18650 Li-ion with 5V Solar MPPT charger.
