"""
hardware/sensor_reader.py
Arun Sharma - Hardware: Sensors, LoRa, Microcontroller & Alarm Integration
SKIT/AI/2023-2027/09

ESP32 / Raspberry Pi sensor data reader for:
  - Rain gauge (tipping bucket)
  - BME280 (temperature, pressure, humidity)
  - LoRa transmission (SX1276)
  - Buzzer/LED alarm output

Sprint 3: Data Collection
"""

import time
import json

# --- Pin Configuration (ESP32) ---
RAIN_GAUGE_PIN   = 34   # Interrupt pin for tipping bucket rain gauge
BUZZER_PIN       = 26   # Active buzzer output
LED_RED_PIN      = 25   # Red alarm LED
I2C_SDA_PIN      = 21   # BME280 I2C SDA
I2C_SCL_PIN      = 22   # BME280 I2C SCL

# 1 tip of bucket = 0.2794 mm of rainfall
BUCKET_SIZE_MM   = 0.2794
LORA_FREQUENCY   = 433e6  # 433 MHz for India

# Tip counter (incremented by interrupt)
_tip_count = 0


def on_rain_tip():
    """ISR callback — called on each rain gauge tip."""
    global _tip_count
    _tip_count += 1


def read_bme280_mock():
    """
    Read temperature, pressure, humidity from BME280.
    Returns dict with sensor values.
    (Replace with actual smbus2 / machine.I2C calls on hardware.)
    """
    # Simulated realistic values for Jaipur hill region
    return {
        "temperature_c": 18.4,
        "pressure_hpa": 1008.3,
        "humidity_pct": 76.5,
    }


def read_rain_mm(reset=True):
    """
    Read accumulated rainfall in mm since last reset.

    Args:
        reset: If True, resets the tip counter after reading.
    Returns:
        Accumulated rainfall in mm.
    """
    global _tip_count
    rain_mm = _tip_count * BUCKET_SIZE_MM
    if reset:
        _tip_count = 0
    return round(rain_mm, 4)


def build_sensor_payload() -> dict:
    """
    Builds a complete sensor data payload for LoRa transmission.

    Returns:
        dict with timestamp, rain_mm, pressure_hpa, humidity_pct.
    """
    bme = read_bme280_mock()
    rain = read_rain_mm(reset=True)

    payload = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "rain_mm":        rain,
        "pressure_hpa":   bme["pressure_hpa"],
        "humidity_pct":   bme["humidity_pct"],
        "temperature_c":  bme["temperature_c"],
    }
    return payload


def trigger_alarm(risk_level: str):
    """
    Activate buzzer and LED based on risk level.
    LOW    -> no alarm
    MODERATE -> slow blink
    HIGH     -> fast blink + short beep
    CRITICAL -> continuous buzzer + solid red LED
    """
    print(f"[ALARM] Risk level: {risk_level}")
    if risk_level == "CRITICAL":
        print(">>> BUZZER ON | RED LED SOLID")
    elif risk_level == "HIGH":
        print(">>> BUZZER BEEP x3 | RED LED FAST BLINK")
    elif risk_level == "MODERATE":
        print(">>> RED LED SLOW BLINK")
    else:
        print(">>> All clear")


def send_lora(payload: dict):
    """
    Serialize payload to JSON and transmit over LoRa SX1276.
    (Replace with actual sx127x driver calls on hardware.)
    """
    msg = json.dumps(payload)
    print(f"[LoRa TX @ {LORA_FREQUENCY/1e6:.0f}MHz] {msg}")


# --- Main loop ---
if __name__ == "__main__":
    print("=== Cloud Burst Sensor Node Starting ===")
    print(f"Rain gauge pin: GPIO{RAIN_GAUGE_PIN}")
    print(f"BME280: SDA=GPIO{I2C_SDA_PIN}, SCL=GPIO{I2C_SCL_PIN}")
    print(f"LoRa frequency: {LORA_FREQUENCY/1e6:.0f} MHz\n")

    while True:
        payload = build_sensor_payload()
        print(f"[Sensor] {payload}")
        send_lora(payload)
        time.sleep(600)   # Transmit every 10 minutes