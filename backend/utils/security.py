def check_payload_size(data: bytes, max_bytes: int = 1024) -> bool:
    return len(data) <= max_bytes
