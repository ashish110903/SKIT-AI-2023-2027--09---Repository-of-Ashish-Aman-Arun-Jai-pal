# Circuit Schematic & Hardware Wiring

- 10k pull-up resistors on I2C SDA/SCL lines
- RC debounce filter (10k resistor + 100nF ceramic cap) across rain gauge reed switch
- 3.3V low-dropout voltage regulator (AMS1117-3.3) for stable sensor VCC
