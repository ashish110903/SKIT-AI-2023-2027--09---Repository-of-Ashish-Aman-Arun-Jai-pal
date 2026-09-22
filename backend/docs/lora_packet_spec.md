# LoRa Telemetry Packet Specification

Header: 4-byte Magic Number (0xCB01)
Payload: 16-byte packed struct (station_id: 2B, rain: 2B, pressure: 4B, temp: 2B, humidity: 2B, CRC: 4B).
