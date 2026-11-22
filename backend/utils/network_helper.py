def verify_checksum(payload: bytes, expected_crc: int) -> bool:
    import binascii
    return binascii.crc32(payload) == expected_crc
