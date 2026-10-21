#ifndef PACKET_SERIALIZER_H
#define PACKET_SERIALIZER_H
#include <stdint.h>

struct __attribute__((packed)) LoRaPacket {
  uint16_t stationId;
  uint16_t rainMmX100;
  uint32_t pressureHpaX100;
  int16_t tempCX100;
  uint16_t humidityX100;
  uint32_t checksum;
};
#endif
