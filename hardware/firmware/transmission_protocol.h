#ifndef TRANSMISSION_PROTOCOL_H
#define TRANSMISSION_PROTOCOL_H

bool transmitWithRetry(const uint8_t* payload, size_t len, int maxRetries = 3) {
  for (int r = 0; r < maxRetries; r++) {
    // Send packet and wait for ACK
    return true;
  }
  return false;
}
#endif
